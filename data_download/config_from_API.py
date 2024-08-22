import os
import sys

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.functions import generate_API_datestamps

# Generate time periods
start_year = 2022
start_month = 10
end_year = 2023
end_month = 3

# Data download specs
models = ['fatalities001']
periods = generate_API_datestamps(start_year, start_month, end_year, end_month)
versions = ['t01']
loas = ['pgm']

# Save path for csv files
home = os.path.expanduser("~")
save_path = f"{home}/Desktop/"