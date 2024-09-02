import pandas as pd
import numpy as np
import os
from viewser import Queryset, Column
import json
import csv

"""
This script preps CSV files downloaded from the VIEWS API from the fatalities001 model, pgm level, for use on the VIEWS dashboard. 
It drops unnecessary columns, strips unnecessary prepends, renames columns to match naming in fatalities002, and applies an inverse 
function for logged values to instead show predicted fatalities. Files are fetched from the folder_path, and edited versions are saved 
to output_folder_path with the original name.

TODOs: refactoring, config files. 
"""

# Define the path to your folder containing CSV files
folder_path = os.path.expanduser("~/ViEWS Dropbox/ViEWS/Dashboards/Dashboard2/flat_files_fatalities001/pgm/original_data/")
output_folder_path = os.path.expanduser("~/ViEWS Dropbox/ViEWS/Dashboards/Dashboard2/flat_files_fatalities001/pgm/edited_data/")
json_output_folder_path = os.path.expanduser("~/ViEWS Dropbox/ViEWS/Dashboards/Dashboard2/flat_files_fatalities001/pgm/edited_data/json/")
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
            key = f"{rows['pg_id']}_{rows['month_id']}"
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

            # Keep only the specified columns
            columns_to_keep = ['pg_id', 'month_id', 'sc_pgm_sb_main', 'sc_pgm_sb_dich_main']
            df = df[columns_to_keep]

            # Drop any column named 'Unnamed: 0' if it exists
            if 'Unnamed: 0' in df.columns:
                df.drop(columns=['Unnamed: 0'], inplace=True)

            # Rename specific columns if they exist
            df.rename(columns={"sc_pgm_sb_dich_main": "main_dich", "sc_pgm_sb_main": "main_mean"}, inplace=True)
            
            # Apply the inverse log transformation to the 'main_mean' column
            if 'main_mean' in df.columns:
                df['main_mean'] = np.exp(df['main_mean']) - 1

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

print('All CSV files are now prepped. Proceeding to merging them with their identifiers...')

print('Fetching queryset for identifiers...')

# Queryset to fetch descriptive identifiers for VIEWS data. Renamed to match names in the VIEWS API. 
pgm_identifiers = (Queryset("fatalities001_API_identifiers_pgm", "priogrid_month")
              # Identifiers
              .with_column(Column('year', from_column='year_id', from_loa='month'))
              .with_column(Column('month', from_column='month', from_loa='month'))
              .with_column(Column('isoab', from_column='isoab', from_loa='country'))
              .with_column(Column('name', from_column='name', from_loa='country'))
              .with_column(Column('gwcode', from_column='gwcode', from_loa='country'))
              .with_column(Column('country_id', from_column='country_id', from_loa='country_month')) # this fetches pg ids
              )

# Fetch the queryset and save it to csv
pgm_identifiers = pgm_identifiers.publish().fetch().reset_index().rename(columns={"priogrid_gid":"pg_id"})
pgm_identifiers.to_csv('pgm_identifiers.csv')

# Iterate over all CSV files in the specified folder
for file_name in os.listdir(output_folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(output_folder_path, file_name)
        
        # Debugging: Print the file path being processed
        print(f"Processing file: {file_path}")

        try:
            # Load the CSV file into a DataFrame
            api_df = pd.read_csv(file_path, index_col=False)
            
            # Merge with identifiers
            final_df = pd.merge(pgm_identifiers, api_df, on=['pg_id', 'month_id'], how='inner').reset_index(drop=True)

            # Save the final merged DataFrame
            final_output_path = os.path.join(output_folder_path, file_name)
            final_df.to_csv(final_output_path, index=False)
            print(f"Merged CSV file saved to {final_output_path}")

            # Convert the merged CSV to JSON
            json_file_name = file_name.replace(".csv", ".json")
            json_file_path = os.path.join(json_output_folder_path, json_file_name)
            make_json(final_output_path, json_file_path)
            print(f"JSON file saved to {json_file_path}")

        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

print('Done!')
