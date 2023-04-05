from prefect_gcp import GcpCredentials
import json

BLOCK_NAME_PLACEHOLDER = "birdblockprefect"

def connect_to_gcp(GCP_CREDENTIALS_JSON: str):
    """ This function will connect to GCP project via JSON key file"""
    with open(GCP_CREDENTIALS_JSON) as cred_file:
        cred_dict = json.load(cred_file)
        GcpCredentials(
            service_account_info=cred_dict
        ).save(f"{BLOCK_NAME_PLACEHOLDER}", overwrite=True)

    gcp_credentials_block = GcpCredentials.load(f"{BLOCK_NAME_PLACEHOLDER}")
    bigquery_client = gcp_credentials_block.get_bigquery_client()
    return (gcp_credentials_block, bigquery_client)

#print(connect_to_gcp("/home/daria/Downloads/taxiworkflow-4cb511a2ae52.json"))
