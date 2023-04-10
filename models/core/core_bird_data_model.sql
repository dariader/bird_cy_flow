{{ config(materialized='table') }}

select scientific_name, lat, lng, year, month, custom_primary_key, observation_date from {{ ref('stg_historical_dbt_model') }}
UNION ALL
select scientific_name, lat, lng, year, month, custom_primary_key, observation_date from {{ ref('stg_realtime_dbt_model') }}
