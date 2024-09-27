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



# CREATE WATCHLIST 1: Highest predicted fatalities in 2025 

# Step 1: Fetch country-month forecasts from API
forecasts = f.fetch_forecasts_from_api('fatalities002_2024_07_t01', 'cm', 'main_mean', False, save_folder)

# Step 2: Aggregate forecasts by country-year, save to csv
forecasts_by_cy = f.forecasts_from_cm_to_cy(forecasts, '2025', True, save_folder)

print('Watchlist 1 successfully created.\n\n')


# CREATE WATCHLIST 2: Highest predicted fatalities in 2025, amongst countries with less than 25 BRDs over the past 12 months

# Step 1: Get sum of actuals for last 12 months
sum_actuals_last_12months = f.get_sum_of_actuals_for_last_12months('predictors_fatalities002_0000_00', 'cm', 'ucdp_ged_sb_best_sum', False, save_folder)

# Step 2: Get list of countries with less than 25 BRDs over last 12 months + sum fatalities for use in function filter_forecasts_by_criteria() 
qualifying_countries = sum_actuals_last_12months[sum_actuals_last_12months['actuals_last_12months'] < 25].copy()

# Step 3: Create watchlist based on criteria above (save as csv)
f.filter_forecasts_by_criteria(forecasts_by_cy, qualifying_countries, True, save_folder)

print('Watchlist 2 successfully created.\n\n')


# CREATE WATCHLIST 3: Predicted relative change in fatalities

# Create watchlists for each category of predicted intensity of violence + all categories combined, save to csv
f.watchlist_relative_change_in_sb_fatalities(forecasts_by_cy, 'predictors_fatalities002_0000_00', "", True, save_folder)

print('Watchlist 3 successfully created.\n\n')

