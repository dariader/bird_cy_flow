{{ config(materialized='view') }}

with historical_source as (
    -- add common name
    select family,
     genus,
      species as scientific_name,
       decimalLatitude as lat,
        decimalLongitude as lng,
         catalogNumber as custom_primary_key,
         cast(eventDate as datetime) as observation_date,
         FORMAT_DATETIME('%Y', PARSE_DATE('%Y', CAST(year AS STRING))) as year,
         FORMAT_DATETIME('%m', PARSE_DATE('%m', CAST(month AS STRING))) as month,
     row_number() over(partition by genus, year) as rn
     from {{source("raw_bird_data", "historical_data")}}
     where taxonRank='SPECIES')
select * from historical_source