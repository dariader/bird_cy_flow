{{ config(materialized='table') }}

with realtime_data as (
    select *,
    from {{ ref('stg_realtime_dbt_model') }}
),
historical_data as (
    select *,
    from {{ ref('stg_historical_dbt_model') }}
)
select * from realtime_data,
full outer join historical_data
on historical_data.custom_primary_key = realtime_data.custom_primary_key;
