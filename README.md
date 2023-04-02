Dependencies: 

1. Prefect
2. DBT
3. Python 3.10
4. GCS, GBQ


Google cloud

1. create workspace and project
2. terraform will create GCS lake and upload file
3. create service account in IAM tab, create and export keys
4. write location of the key into BIRDFLOW_GOOGLE_KEY variable
BIRDFLOW_GOOGLE_KEY="/home/daria/Downloads/birdflow-5be52b02fe39.json"

dbt: 
in the folder: 
1. run sudo docker compose build
2. docker compose run dbt-birdflow init