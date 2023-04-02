"""
This Prefect flow will update the GCS (remove all previous data if necessary):
will populate GCS with new data
"""


@task()
def search_for_new_data(self):
    pass

@task()
def load_new_data_gcs(self):
    pass

@flow
def main():
    connector = connect_to_gcp()
    self.search_for_new_data()
