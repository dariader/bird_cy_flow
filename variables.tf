locals {
  data_lake_bucket = "dtc_data_lake_us"
  project = "birdflow"
  historical_bird_file = "./data/0163061-220831081235567.csv"
  gcs_bucket = "${local.data_lake_bucket}_${local.project}"
  historical_data_name = "historical_bird_data"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default     = "US"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type        = string
  default     = "bird_data_test"
}
