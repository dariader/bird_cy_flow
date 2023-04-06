{{ config(materialized='view') }}


with realtime_source as (
    -- parse sci name into genus and family
    select
    comName as common_name,
     sciName as scientific_name,
      lat,
       lng,
        cast(custom_primary_key as string) as custom_primary_key,
        obsDt as observation_date,
        date_trunc(observation_date, year) as year,
        date_trunc(observation_date, year) as month,
        from {{source("bird_data_test", "realtime_data")}}
) select * from realtime_source limit 151
