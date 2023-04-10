{{ config(materialized='view') }}


with realtime_source as (
    -- parse sci name into genus and family
    select
    comName as common_name,
     sciName as scientific_name,
      lat,
       lng,
        cast(custom_primary_key as string) as custom_primary_key,
        cast(obsDt as datetime) as observation_date, -- 2023-04-04 13:00
        FORMAT_DATETIME('%Y', cast(obsDt as datetime format "YYYY-MM-DD HH24:MI")) as year,
        FORMAT_DATETIME('%m', cast(obsDt as datetime format "YYYY-MM-DD HH24:MI")) as month,
        from {{source("raw_bird_data", "realtime_data")}}
) select * from realtime_source limit 151
