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
export BIRDFLOW_GOOGLE_KEY="/home/daria/Downloads/birdflow-5be52b02fe39.json"

dbt: 
man:
https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/dbt_cloud_setup.md
in the folder: 
1. run sudo docker compose build
2. docker compose run dbt-birdflow init

prefect: 
install requirements prefect_scheduler/requirements.txt
prefect orion start
#run launch_bird_flow_prefect.py to init flow
see http://127.0.0.1:4200

in crontab:
*/2 * * * * python3 /home/daria/PycharmProjects/bird_cy_flow/src/launch_bird_flow_prefect.py

