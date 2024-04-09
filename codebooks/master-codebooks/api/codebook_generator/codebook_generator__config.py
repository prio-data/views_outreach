"""
This file contains all parameters required to instruct the 
markdown (.md) codebook generator on:

- What source JSON codebook to use (API or local file)
- What type of output it will generate (codebook for forecasts or predictor output)
- What run the codebook concerns (for forecasts only)

Make your changes below, save, and then run the Codebook Generator script to produce the .md material.
"""

# Are you creating a codebook for forecast data or predictor data? 
# Choose "predictors" or "forecasts"
outcome_type = "predictors" 

# How are you loading the JSON version of the codebook?
# Choose "api" or "file"
fetch_type = "file" # api or file

# Where do you want to save your PDF file? Default is the VIEWS Dropbox under Codebooks/PDFs. 
home = os.path.expanduser("~") # Don't change this line
save_path = home + "/ViEWS Dropbox/ViEWS/Codebooks/PDFs/" # Edit here

# If you are generating a codebook for PREDICTOR data, you are 
# done here. No more edits needed. 

# If you are generating a codebook for FORECAST data, enter the run ID below:
run = "fatalities002_2024_02_t01"

