{{ config(materialized='table') }}

select scientific_name, lat, lng, custom_primary_key from {{ ref('stg_historical_dbt_model') }}
UNION ALL
select scientific_name, lat, lng, custom_primary_key from {{ ref('stg_realtime_dbt_model') }}
