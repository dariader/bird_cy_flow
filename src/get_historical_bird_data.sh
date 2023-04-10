#!/bin/bash
# prerequesites for job creation: account on https://www.gbif.org
# variables username and password are stored in bashrc file

#if you need to recreate a job:
#this will recreate an id of the new dataset
#FILE="${curl --user $GBIF_USER:$GBIF_PASSW --header "Content-Type: application/json" --data @query.json https://api.gbif.org/v1/occurrence/download/request}.zip"

# default: recreation of db this zip should be available for anyone with the link
# this will check whether dataset with the same name is present in the folder

# if you are recreating a job, comment next line.
FILE="0133998-220831081235567.zip"

if [ -f $FILE ]; then
   echo "Dataset exists."
else
   echo "Dataset does not exist."
   curl --location --remote-name https://api.gbif.org/v1/occurrence/download/request/$FILE
fi

