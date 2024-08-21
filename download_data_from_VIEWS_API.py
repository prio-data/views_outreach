import requests
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configs import config_dataset_from_api as config
from utils.functions import download_dataset_from_api

download_dataset_from_api(config.models, config.periods, config.versions, config.loas, config.save_path)