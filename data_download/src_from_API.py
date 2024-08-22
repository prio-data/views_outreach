import requests 
import pandas as pd
import os
import sys
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import data_download.config_from_API as config
from utils.functions import download_data_from_api

download_data_from_api(config.models, config.periods, config.versions, config.loas, config.save_path)
