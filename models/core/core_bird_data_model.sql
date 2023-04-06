{{ config(materialized='table') }}

select * from {{ ref('stg_historical_dbt_model') }}
UNION ALL
select * from {{ ref('stg_realtime_dbt_model') }}
