from src.connect_gcp import connect_to_gcp


class BirdData:
    """
    This class will initialise the GCS (remove all previous data if necessary):
    will populate GCS with archive data
    """
    def __init__(self):
        connector = connect_to_gcp()
        self.load_old_data_to_gcs()

    def load_old_data_to_gcs(self):

        pass

