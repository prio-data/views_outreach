# Create data for the PRIO Annual Report. 

import requests
import pandas as pd
import os
import sys
from pathlib import Path
import numpy as np

# Add the parent directory ('views_outreach') to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
root_dir  = Path(os.path.abspath(os.path.join(os.path.dirname(__file__)))).parent.absolute()
sys.path.append(root_dir)

from utils import functions as f

# CONFIG: This should go in a config file at some point

# Get the directory where the notebook is running, save to folder in absolute path
current_dir = os.getcwd()
save_folder = f'{current_dir}/prio_annual_report/data/'

# Ensure the save folder exists
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# CREATE WATCHLIST 1: Highest predicted fatalities in 2025 

# Step 1: Fetch country-month forecasts from API
forecasts = f.fetch_data_from_api(api_call='https://api.viewsforecasting.org/fatalities002_2024_07_t01/cm/sb/main_mean', csv=False, save_path=save_folder)

# Step 2: Aggregate forecasts by country-year, save to csv
forecasts_by_cy = f.forecasts_from_cm_to_cy(forecasts=forecasts, year='2025', csv=True, save_path=save_folder)

print('Watchlist 1 successfully created.\n\n')


# CREATE WATCHLIST 2: Highest predicted fatalities in 2025, amongst countries with less than 25 BRDs over the past 12 months

# Step 1: Get latest actuals for all countries
predictor_df = f.fetch_data_from_api(api_call='https://api.viewsforecasting.org/predictors_fatalities002_0000_00/cm/px/ucdp_ged_sb_best_sum', csv=False, save_path=save_folder)

# Step 2: Get sum of actuals for last 12 months
sum_actuals_last_12months_by_c = f.get_sum_of_actuals_last_12months_by_c(predictor_df=predictor_df, feature='ucdp_ged_sb_best_sum', csv=False, save_path=save_folder)

# Step 3: Get list of countries with less than 25 BRDs over last 12 months + sum fatalities for use in function filter_forecasts_by_criteria() 
qualifying_countries_df = sum_actuals_last_12months_by_c[sum_actuals_last_12months_by_c['actuals_last_12months'] < 25].copy()

# Step 4: Create watchlist based on criteria above (save as csv)
f.filter_forecasts_by_criteria(forecasts_df=forecasts_by_cy, qualifying_countries_df=qualifying_countries_df, csv=True, save_path=save_folder)

print('Watchlist 2 successfully created.\n\n')


# CREATE WATCHLIST 3: Predicted relative change in fatalities

# Create watchlists for each category of predicted intensity of violence + all categories combined, save to csv
f.watchlist_relative_change_in_fatalities(forecasts_by_cy=forecasts_by_cy, sum_actuals_last_12months_by_c=sum_actuals_last_12months_by_c, category="", csv=True, save_folder=save_folder)

print('Watchlist 3 successfully created.\n\n')

