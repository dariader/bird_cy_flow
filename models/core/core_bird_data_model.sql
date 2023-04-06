{{ config(materialized='table') }}

with realtime_data as (
    select *,
    from {{ ref('stg_realtime_dbt_model') }}
),
historical_data as (
    select *,
    from {{ ref('stg_historical_dbt_model') }}
)
select * from realtime_data
UNION ALL
select * historical_data
