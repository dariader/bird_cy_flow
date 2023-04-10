# BirdFlow
An app to view the location of birds on Cyprus

https://dariader.github.io/bird_cy_flow/

### Dependencies:

1. Prefect
2. DBT(Cloud)
3. Python 3.10
4. GCS, GBQ access
Run:
`pip install -r /src/requirements.txt`

### Schema of the project
![Schema](./src/app/schema.png)
Steps: 
1. Upload historical data to GCS and BQ
2. Set up a regular cron job to schedule downloads of data from ebird database
3. Set up a DBT cloud, schedule a job to periodically regenerate dataset to update the present data 
4. Using Looker and core_bird_data_model schema create a dashboard
5. Share dashboard as a widget and integrate into github.io. Code of webpage is index.html.  

## HOW TO RUN: 
### Get Data
#### Archive data
A) Must be retrieved from GBIF. They consolidate data for a large period (each several months). 
For that you need: 
1) register in GBIF -- get password and username
2) ask for permission to load data (cyprus data)
3) download and put this data in ./data/ folder. See code for that in `/src/get_historical_data.sh`
4) edit config.yaml file section: 

```commandline
### folders
folders:
  historical_data_folder: "../data/<NAME>.csv"
```

B) OR you request access to the data from myself (for my project reviewers only). 
link to google drive: 
https://drive.google.com/file/d/1Z0Tz1MQfz92sdxF6Pz1jz0050d14FxJF/view?usp=share_link

#### Realtime data
This data is retrieved from ebird servers, which are updated ~each hour. 
To be able to source data from ebird, you need to 
1) register here: https://ebird.org/home
2) get api key, put it in the config file (config.yaml)

### Set up Google cloud
1. create workspace and project, put names into config.yaml AND variables.tf
```Config yaml
gcp_project:
  title: birdflow
  bucket_name: dtc_data_lake_us_birdflow
  gbq_dataset_raw: raw_bird_data
  gbq_dataset_processed: processed_bird_data
```
```Terraform
locals {
  data_lake_bucket = "dtc_data_lake_us" # GCS bucket name
  project = "birdflow" # project name
  historical_bird_file = "./data/0163061-220831081235567.csv" # location of historical data
  historical_data_name = "historical_bird_data" # DO NOT CHANGE
  gcs_bucket = "${local.data_lake_bucket}_${local.project}"  # DO NOT CHANGE
}
```

2. create service account in IAM tab, create and export json keys
3. create environment variable GOOGLE_APPLICATION_CREDENTIALS and write the path to the json with GCP credentials
4. write location of json keys to config.yaml

### Terraform 
1. terraform will create GCS lake and upload historical observations file
run: 
` terraform plan `
` terraform apply `

### Cron job
Set as working directory the directory of the project.
run:
`/usr/bin/crontab /src/prefect_scheduler/schedule`
This will launch cron job with the parameters in the `schedule` file

or add the contents of `/src/prefect_scheduler/schedule`
in the prompt of `crontab -e` command
### Cron job monitoring
run
`prefect orion start`