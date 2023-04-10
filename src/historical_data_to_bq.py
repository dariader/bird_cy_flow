import pandas as pd

from src.utils.config import Config
from src.utils.connect_gcp import connect_to_gcp

GCP_CREDENTIALS = Config('../../config.yaml').credentials.get('gcp_creds_file', KeyError)
HISTORICAL_DATA = Config('../../config.yaml').folders.get('historical_data_folder', KeyError)
PROJECT_NAME = Config('../../config.yaml').gcp_project.get('title', KeyError)
GCS_BUCKET_NAME = Config('../../config.yaml').gcp_project.get('bucket_name', KeyError)
GBQ_DATASET_NAME = Config('../../config.yaml').gcp_project.get('gbq_dataset_raw', KeyError)

def load_historical_data_GBQ(dataframe, mode='append'):
    """This will load historical data to GBQ table"""
    gcp_credentials_block, bigquery_client = connect_to_gcp(GCP_CREDENTIALS)
    print('Inserting..')
    dataframe.to_gbq(
        destination_table=f"{GBQ_DATASET_NAME}.historical_data",
        project_id=PROJECT_NAME,
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists=mode,
    )


if __name__ == "__main__":
    historical_df = pd.read_table(HISTORICAL_DATA, chunksize=1000)
    load_historical_data_GBQ(next(historical_df), mode='replace')
    while True:
        print('Inserting next chunk..')
        load_historical_data_GBQ(next(historical_df), mode='append')
