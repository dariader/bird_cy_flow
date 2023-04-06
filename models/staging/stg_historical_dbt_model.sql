{{ config(materialized='view') }}

with historical_source as (
    -- add common name
    select family, genus, species as scientific_name, decimalLatitude as lat, decimalLongitude as lng, catalogNumber as custom_primary_key, year, month, row_number() over(partition by genus, year) as rn
     from {{source("bird_data_test", "historical_data")}}
     where taxonRank='SPECIES')
select * from historical_source