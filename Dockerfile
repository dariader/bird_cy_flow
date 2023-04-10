FROM python:3.10.11-slim
COPY ./src /src
COPY config.yaml config.yaml
COPY /creds/*.json /src/gcp_creds.json
RUN apt-get update && apt-get -y install cron
RUN pip install -r src/requirements.txt
EXPOSE 4200
#COPY src/prefect_scheduler/schedule /etc/cron.d/schedule # this will launch cron job to load realtime bird data
RUN prefect orion start
RUN /usr/bin/crontab /src/prefect_scheduler/schedule