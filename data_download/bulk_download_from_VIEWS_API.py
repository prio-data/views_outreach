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

# Get the directory where the notebook is running, save to folder in absolute path
current_dir = os.getcwd()
save_folder = f'{current_dir}/downloads/'

# Ensure the save folder exists
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

#-------------------------------------------
# Select models of interest
models = ['fatalities001', 'fatalities002']

# Select first and last run/dataset to fetch
periods = f.generate_API_datestamps(start_year=2021, start_month=12, end_year=2024, end_month=12) 

# Select dataset versions. t01 is the first and default run; t02 versions are published in case of errors in the first run
versions = ['t01', 't02'] 

# Select levels of analysis
loas = ['cm', 'pgm']

# Select where to save the datasets. By default, files are saved in a 'downloads' folder in this respository. To change, edit the cell above. 
save_path = save_folder 
#-------------------------------------------

# Fetch and download the forecasts (do not change)
f.download_multiple_forecasts_from_api(models, periods, versions, loas, save_path)

print('All done! Your files should now be available in the downloads folder in the same repository as this script.')