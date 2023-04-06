import pandas as pd
from src.utils.connect_gcp import connect_to_gcp


def load_historical_data_GBQ(dataframe, mode='append'):
    """This will load historical data to GBQ table"""
    #creds = os.getenv('BIRDFLOW_GOOGLE_KEY')
    creds = "/home/daria/Downloads/birdflow-5be52b02fe39.json"
    gcp_credentials_block, bigquery_client = connect_to_gcp(creds)
    print('Inserting..')
    dataframe.to_gbq(
        destination_table="bird_data_test.historical_data",
        project_id="birdflow",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists=mode,
    )


if __name__ == "__main__":
    historical_df = pd.read_table("../data/0163061-220831081235567.csv", chunksize=1000)
    load_historical_data_GBQ(next(historical_df), mode='replace')
    while True:
        print('Inserting next chunk..')
        load_historical_data_GBQ(next(historical_df), mode='append')