import json
import requests


file_type = "predictors" # predictors or forecasts

fetch_type = "url" # url or file

run = "predictors_fatalities002_0000_00" # fatalities002_2024_02_t01

url_codebook = "https://api.viewsforecasting.org/"+run+"/codebook"

codebook_name = "codebook_" + file_type + "_" + run + "_from_" + fetch_type + ".md"

if file_type == "forecasts":
        file_path = "codebook_fatalities002_forecasts.json"  # Specify the path to your JSON file
if file_type == "predictors":
        file_path = "codebook_fatalities002_predictors.json"  # Specify the path to your JSON file

def generate_markdown(data, depth=0):
    markdown_content = ""
    for key, value in data.items():
        if depth == 0:
            markdown_content += f"## {key}\n\n"
        if isinstance(value, dict):
            markdown_content += f"{'  ' * (depth - 1)}- **{key}**:\n"
            markdown_content += generate_markdown(value, depth=depth+1)
        else:
            markdown_content += f"{'  ' * (depth - 1)}- **{key}**: {value}\n"
    return markdown_content

def main_file():
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            markdown_content = generate_markdown(json_data)
            if file_type == "forecasts":
                with open(codebook_name, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
            if file_type == "predictors":
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
        if file_type == "forecasts":
                with open(codebook_name, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
        if file_type == "predictors":
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

