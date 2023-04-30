"""
This Prefect flow will update the GCS (remove all previous data if necessary):
will populate GCS with new data
"""
import os

import pandas as pd
from datetime import datetime, timedelta
from prefect import task, Flow, get_run_logger
from prefect_gcp import GcsBucket
from prefect import flow

from utils.config import Config
from utils.connect_gcp import connect_to_gcp
from utils.find_new_bird_data import retrieve_data

GCP_CREDENTIALS = Config('../../config.yaml').credentials.get('gcp_creds_file', KeyError)
PROJECT_NAME = Config('../../config.yaml').gcp_project.get('title', KeyError)
GCS_BUCKET_NAME = Config('../../config.yaml').gcp_project.get('bucket_name', KeyError)
GBQ_DATASET_NAME = Config('../../config.yaml').gcp_project.get('gbq_dataset_raw', KeyError)
@task()
def search_for_new_data():
    logger = get_run_logger()
    """This task will load data from ebird, last 1 day"""
    query = retrieve_data(2)

    if len(query) < 1:
        logger.info('No new data')
    else:
        logger.info('New data!')
        logger.info(f'Data size is {len(query)}')
        df = pd.DataFrame(query)
        time_now = datetime.now()
        df['loading_date'] = time_now
        df['custom_primary_key'] = df.apply(lambda x: hash(tuple(x)), axis=1)
        path = f"{os.getcwd()}/data/realtime"
        os.makedirs(path, exist_ok=True)
        filename = f"{path}/{time_now}.parquet"  # folders are created automatically
        logger.info(filename)
        df.to_parquet(filename)
        return filename, df


@task()
def load_new_data_GCS(file_path):
    """This will load new data to GCS folder"""
    logger = get_run_logger()
    gcp_credentials_block, bigquery_client = connect_to_gcp(GCP_CREDENTIALS)
    logger.info('Connecting to GCS')
    gcs_bucket = GcsBucket(
        bucket=GCS_BUCKET_NAME,
        gcp_credentials=gcp_credentials_block
    )
    logger.info('Loading new data to GCS')
    gcs_bucket.upload_from_path(file_path)


@task()
def load_new_data_GBQ(dataframe):
    """This will load new data to GBQ table"""
    logger = get_run_logger()
    logger.info('Connecting to GBQ')
    gcp_credentials_block, bigquery_client = connect_to_gcp(GCP_CREDENTIALS)
    logger.info('Loading new data to GBQ')
    dataframe.to_gbq(
        destination_table=f"{GBQ_DATASET_NAME}.realtime_data",
        project_id=PROJECT_NAME,
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )


@flow()
def prefect_flow():
    output = search_for_new_data()
    if output is not None:
        file_path = output[0]
        dataframe = output[1]
        load_new_data_GCS(file_path)
        load_new_data_GBQ(dataframe)


if __name__ == "__main__":
    prefect_flow()
# prefect orion start
