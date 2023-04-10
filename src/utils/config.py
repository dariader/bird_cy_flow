"""
This class will parse config into dict for easier access to credentials, etc
"""
import yaml

class Config:
    def __init__(self, config_path):
        self.config=self.read(config_path)
        self.credentials = self.config['credentials']
        self.folders = self.config['folders']
        self.gcp_project = self.config['gcp_project']

    def read(self, config_path):
        with open(config_path) as yaml_file:
            config_dict = yaml.safe_load(yaml_file)
        return config_dict

