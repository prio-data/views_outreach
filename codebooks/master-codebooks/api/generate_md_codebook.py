import json
import requests

"""
Start by changing the config settings below to tell the script whether you're writing:

1) A codebook for output from forecasts or predictors
2) If you're fetching the JSON version of this codebook from the VIEWS API or from a local file
3) What run ID to tailor the codebook for
"""

# Are you creating a codebook for forecast data or predictor data? 
# Choose "predictors" or "forecasts"
outcome_type = "predictors" 

# How are you loading the JSON version of the codebook?
# Choose "url" or "file"
fetch_type = "url" # url or file

# What run ID are you writing the codebook for? 
# This is used to find the correct JSON codebook, and to name the .md output file. 
run = "predictors_fatalities002_0000_00" # fatalities002_2024_02_t01


"""
Execution starts here. No edits needed.
"""

url_codebook = "https://api.viewsforecasting.org/"+run+"/codebook"

codebook_name = "codebook_" + outcome_type + "_" + run + "_from_" + fetch_type + ".md"

if outcome_type == "forecasts":
        file_path = "codebook_fatalities002_forecasts.json"  # Specify the path to your JSON file
if outcome_type == "predictors":
        file_path = "codebook_fatalities002_predictors.json"  # Specify the path to your JSON file

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

def main_file():
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            markdown_content = generate_markdown(json_data)
            if outcome_type == "forecasts":
                with open(codebook_name, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
            if outcome_type == "predictors":
                with open(codebook_name, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
            print("Markdown file from local json file generated successfully!")
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")

def main_url():
    response = requests.get(url_codebook)
    if response.status_code == 200:
        json_data = response.json()
        markdown_content = generate_markdown(json_data)
        if outcome_type == "forecasts":
                with open(codebook_name, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
        if outcome_type == "predictors":
            with open(codebook_name, "w", encoding="utf-8") as f:
                f.write(markdown_content)
        print("Markdown file from url generated successfully!")
    else:
        print("Failed to fetch data from the provided URL.")

if __name__ == "__main__":
    if fetch_type == "file":
        main_file()
    if fetch_type == "url":
        main_url()
