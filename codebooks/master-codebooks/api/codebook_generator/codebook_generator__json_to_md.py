import json
import requests
import os

"""
Before running this script, please go the config file and 
customize your settings to generate the codebook based on 
the source file of interest, and to choose your save path. 

No edits are needed within this file.

The script will print out what it has done, and where the 
new codebook has been saved, when the script is finished.
"""

with open(os.path.join(os.path.dirname(__file__), 'codebook_generator__config.py'), 'r') as f:
    exec(f.read())

if outcome_type == "predictors":
    run = "predictors_fatalities002_0000_00"
else: run = run

url_codebook = "https://api.viewsforecasting.org/"+run+"/codebook"

# Specifies where to save the produced codebooks, and by which name
codebook_name = "codebook_" + outcome_type + "_" + run + "_from_" + fetch_type + ".md"
codebook_path = os.path.join(save_path, codebook_name)

# Gets the dirname of the parent dir to where the script is located
dirname = os.path.dirname(__file__)
parent_dirname = os.path.abspath(os.path.join(dirname, os.pardir))

# Creates file paths to the local JSON files (codebooks), currently 
# stored in the parentdir of the running scipt
if outcome_type == "forecasts":
    file_path = os.path.join(parent_dirname, "codebook_fatalities002_forecasts.json")
if outcome_type == "predictors":
    file_path = os.path.join(parent_dirname, "codebook_fatalities002_predictors.json")

def generate_markdown(data, depth=0):
    markdown_content = ""
    first_key_processed = False
    for key, value in data.items():
        if depth == 0:
            if not first_key_processed:
                first_key_processed = True
            else:
                markdown_content += "\n"  # Add a new line before each new key at depth=0 after the first key
            markdown_content += f"## {key}\n\n"
        if isinstance(value, dict):
            if depth > 0:  # If depth is greater than 0, print the key only in h2 tag
                markdown_content += f"{'  ' * (depth - 1)}- **{key}**:\n"
            markdown_content += generate_markdown(value, depth=depth+1)
        else:
            markdown_content += f"{'  ' * depth}- **{key}**: {value}\n"  # Adjusted indentation here
    return markdown_content

def generate_codebook_from_file():
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            markdown_content = generate_markdown(json_data)
            if outcome_type == "forecasts":
                with open(codebook_path, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
            if outcome_type == "predictors":
                with open(codebook_path, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
            print(f"\nMarkdown file for {outcome_type} generated successfully from local file!\nIt is saved to {save_path}.")
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")

def generate_codebook_from_api():
    response = requests.get(url_codebook)
    if response.status_code == 200:
        json_data = response.json()
        markdown_content = generate_markdown(json_data)
        if outcome_type == "forecasts":
            with open(codebook_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
        if outcome_type == "predictors":
            with open(codebook_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
        print(f"\nMarkdown file from {outcome_type} generated successfully from the VIEWS API!\nIt is saved to {save_path}.")
    else:
        print("Failed to fetch data from the provided URL.")

if __name__ == "__main__":
    if fetch_type == "file":
        generate_codebook_from_file()
    if fetch_type == "api":
        generate_codebook_from_api()
