import json
import requests
from pathlib import Path #preferred to os.path
parent_dirname = Path(__file__).resolve().parent.parent #goes up two levels

from codebook_generator__config import outcome_type, fetch_type, save_path, run #change parameters in this file located in same folder

def set_paths_url(run, outcome_type, fetch_type, save_path, parent_dirname):
    """ 
    Function to generate the URL, codebook path, and file path based on the input parameters.
    """
    url_codebook = f"https://api.viewsforecasting.org/{run}/codebook"

    codebook_name = f"codebook_{outcome_type}_{run}_from_{fetch_type}.md"
    codebook_path = Path(save_path) / codebook_name

    file_name = f"codebook_fatalities002_{outcome_type}.json" 
    file_path = Path(parent_dirname) / "master-codebooks" / "api" / file_name

    return url_codebook, codebook_path, file_path

def get_json_codebook():
    """
    Function to fetch existing JSON codebook from the API or local file based on the fetch_type, and return json file.

    Args:
    fetch_type (str): The method to fetch the codebook data - 'api' or 'file'.

    url_codebook (str): The URL to fetch the codebook data from the API.
    OR
    file_path (str): The path to the local file containing the codebook data.

    Returns:
    json_data (dict): The JSON data fetched from the API or local file.
    """
    if fetch_type == "api":
        response = requests.get(url_codebook)
        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            raise Exception("Failed to fetch data from the provided URL.")
    elif fetch_type == "file":
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
                return json_data
        except FileNotFoundError:
            raise Exception("File not found.")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON format.")
    else:
        raise Exception("Invalid fetch type. Choose 'api' or 'file'.")

def convert_to_markdown(data, depth=0): #formerly generate_markdown
    """
    Convert nested dictionary data to Markdown format.

    Parameters:
        data (dict): The nested dictionary containing the data to be converted to Markdown.
        depth (int): The depth of nesting in the dictionary (default is 0).

    Returns:
        markdown_content (str): Markdown content generated from the nested dictionary.
    """
    markdown_content = "" # Initialize an empty string to store the Markdown content
    first_key_processed = False # Flag to check if the first key at depth=0 has been processed
    for key, value in data.items(): # Iterate through the key-value pairs in the dictionary
        if depth == 0: 
            if not first_key_processed: # Check if the first key at depth=0 has been processed
                first_key_processed = True 
            else: # Add a new line before each new key at depth=0 after the first key
                markdown_content += "\n"  
            markdown_content += f"## {key}\n\n" # Add the key as a header in the Markdown content
        if isinstance(value, dict): # Check if the value is a nested dictionary
            if depth > 0:  # If depth is greater than 0, print the key only in h2 tag
                markdown_content += f"{'  ' * (depth - 1)}- **{key}**:\n" # Add the key as a bold item in the Markdown content
            markdown_content += convert_to_markdown(value, depth=depth+1) # Recursively call the function for nested dictionaries
        else: # If the value is not a dictionary
            markdown_content += f"{'  ' * depth}- **{key}**: {value}\n"  # Add the key-value pair to the Markdown content
    return markdown_content

def save_markdown_file(markdown_content, codebook_path):
    """
    Save the Markdown content to a file.

    Parameters:
        markdown_content (str): The Markdown content to be saved.
        codebook_path (str): The path to save the Markdown file.
    """
    with open(codebook_path, "w", encoding="utf-8") as f: # Open the file in write mode
        f.write(markdown_content) # Write the Markdown content to the file

if __name__ == "__main__":
    url_codebook, codebook_path, file_path = set_paths_url(run, outcome_type, fetch_type, save_path, parent_dirname)
    json_data = get_json_codebook()
    markdown_content = convert_to_markdown(json_data)
    save_markdown_file(markdown_content, codebook_path)
    print(f"\nMarkdown file for {outcome_type} generated successfully from {fetch_type}!\nIt is saved to {save_path}.")