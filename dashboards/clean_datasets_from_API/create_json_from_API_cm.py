import pandas as pd
import numpy as np
import os
import json
import csv

"""
This script preps CSV files downloaded from the VIEWS API from the fatalities001 model, cm level, for use on the VIEWS dashboard. 
It drops unnecessary columns, strips unnecessary prepends, renames columns to match naming in fatalities002, and applies an inverse 
function for logged values to instead show predicted fatalities. Files are fetched from the folder_path, and edited versions are saved 
to output_folder_path with the original name, also converted to JSON format.

TODOs: refactoring, config files. 
"""

# Define the path to your folder containing CSV files
folder_path = os.path.expanduser("~/ViEWS Dropbox/ViEWS/Dashboards/Dashboard2/flat_files_fatalities001/cm/original_data/")
output_folder_path = os.path.expanduser("~/ViEWS Dropbox/ViEWS/Dashboards/Dashboard2/flat_files_fatalities001/cm/edited_data/")
json_output_folder_path = os.path.expanduser("~/ViEWS Dropbox/ViEWS/Dashboards/Dashboard2/flat_files_fatalities001/cm/edited_data/json/")

# Ensure output folders exist
os.makedirs(output_folder_path, exist_ok=True)
os.makedirs(json_output_folder_path, exist_ok=True)

# Function to convert a CSV to JSON
def make_json(csvFilePath, jsonFilePath):
    data = {}

    # Open a CSV reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary and add it to data
        for rows in csvReader:
            # Assuming a column named 'No' to be the primary key, replace with relevant key
            # Use a concatenation of 'pg_id' and 'month_id' as the key for each entry
            key = f"{rows['country_id']}_{rows['month_id']}"
            data[key] = rows

    # Open a JSON writer and use json.dumps() function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

# Iterate over all CSV files in the specified folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)

        # Debugging: Print the file path being processed
        print(f"Processing file: {file_path}")

        try:
            # Load the CSV file into a DataFrame, skipping any index column
            df = pd.read_csv(file_path, index_col=False)

            # Drop any column named 'Unnamed: 0' if it exists
            if 'Unnamed: 0' in df.columns:
                df.drop(columns=['Unnamed: 0'], inplace=True)

            # Iterate over the columns and rename where necessary
            for column in df.columns:
                if column.startswith("sc_cm_sb_") and "dich_main" not in column:
                    # Create the new column name by stripping "sc_cm_sb_" from the original column name
                    stripped_column_name = column.replace("sc_cm_sb_", "")
                    
                    # Apply the inverse transformation and rename the column
                    df.rename(columns={column: stripped_column_name}, inplace=True)
                    df[stripped_column_name] = np.exp(df[stripped_column_name]) - 1
                else:
                    print(f"Skipping column: {column} in file: {file_name}")

            # Rename specific columns if they exist
            df.rename(columns={"sc_cm_sb_dich_main": "main_dich", "main": "main_mean"}, inplace=True)

            # Drop the 'surrogate_topic10' column if it exists
            if 'surrogate_topic10' in df.columns:
                df.drop(columns=['surrogate_topic10'], inplace=True)

            # Drop all columns that start with "surrogate_"
            df = df.loc[:, ~df.columns.str.startswith("surrogate_")]

            # Save the modified DataFrame to a new CSV file
            output_file_path = os.path.join(output_folder_path, file_name)
            df.to_csv(output_file_path, index=False)
            print(f"Transformed CSV file saved to {output_file_path}")

            # Convert the modified CSV to JSON
            json_file_name = file_name.replace(".csv", ".json")
            json_file_path = os.path.join(json_output_folder_path, json_file_name)
            make_json(output_file_path, json_file_path)
            print(f"JSON file saved to {json_file_path}")

        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

print('Done processing all files!')
