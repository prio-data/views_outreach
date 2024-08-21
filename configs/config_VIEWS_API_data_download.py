import os
from utils.functions import generate_yearmonth_datestamps

# Generate time periods
start_year = 2022
start_month = 1
end_year = 2023
end_month = 3

# Data download specs
models = ['fatalities001']
periods = generate_yearmonth_datestamps(start_year, start_month, end_year, end_month)
versions = ['t01']
loas = ['pgm']

# Save path for csv files
home = os.path.expanduser("~")
save_path = f"{home}/Desktop/"
