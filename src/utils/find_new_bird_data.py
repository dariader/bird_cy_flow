"""
This script will find and download new bird observation data from ebif API
"""

from ebird.api import get_observations
from config import Config
import os


api_key = Config('../../config.yaml').credentials.get('ebird_api_key', KeyError)

def retrieve_data(last_n_days, location_code="CY"):
    """
    Function to download new data from ebird db
    :param last_n_days: how many days to load from ebird, max 30
    :param location_code: default: CY.
    :return: records in json
    """
    records = get_observations(api_key, location_code, back=last_n_days)
    return records
