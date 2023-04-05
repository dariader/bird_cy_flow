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
from utils.connect_gcp import connect_to_gcp
from utils.find_new_bird_data import retrieve_data


@task()
def search_for_new_data():
    logger = get_run_logger()
    """This task will load data from ebird, last 1 day"""
    query = retrieve_data(2)
    if len(query) < 1:
        logger.info('No new data')
    else:
        logger.info('New data!')
        df = pd.DataFrame(query)
        filename = f"{os.getcwd()}/data/realtime/{datetime.now()}.parquet"# folders are not created by themselves
        logger.info(filename)
        df.to_parquet(filename)
        return filename, df


@task()
def load_new_data(file_path):
    """This will load data to GCS and GBQ"""
    logger = get_run_logger()
    #creds = os.getenv('BIRDFLOW_GOOGLE_KEY')
    creds = "/home/daria/Downloads/birdflow-5be52b02fe39.json"
    logger.info(creds)
    gcp_credentials_block, bigquery_client = connect_to_gcp(creds)
    gcs_bucket = GcsBucket(
        bucket="dtc_data_lake_us_birdflow",
        gcp_credentials=gcp_credentials_block
    )
    gcs_bucket_path = gcs_bucket.upload_from_path(file_path)

@task()
def load_new_data_GCS(file_path):
    """This will load new data to GCS folder"""
    logger = get_run_logger()
    #creds = os.getenv('BIRDFLOW_GOOGLE_KEY')
    creds = "/home/daria/Downloads/birdflow-5be52b02fe39.json"
    logger.info(creds)
    gcp_credentials_block, bigquery_client = connect_to_gcp(creds)
    gcs_bucket = GcsBucket(
        bucket="dtc_data_lake_us_birdflow",
        gcp_credentials=gcp_credentials_block
    )
    gcs_bucket.upload_from_path(file_path)

@task()
def load_new_data_GBQ(dataframe):
    """This will load new data to GBQ table"""
    logger = get_run_logger()
    #creds = os.getenv('BIRDFLOW_GOOGLE_KEY')
    creds = "/home/daria/Downloads/birdflow-5be52b02fe39.json"
    logger.info(creds)
    gcp_credentials_block, bigquery_client = connect_to_gcp(creds)
    dataframe.to_gbq(
        destination_table="bird_data_test.realtime_data",
        project_id="birdflow",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
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