{{ config(materialized='view') }}
SELECT
 family,
     genus,
      species as scientific_name,
       decimallatitude as lat,
        decimallongitude as lng,
         occurrenceid as custom_primary_key,
         cast(eventdate as datetime) as observation_date,
         FORMAT_DATETIME('%Y', PARSE_DATE('%Y', CAST(year AS STRING))) as year,
         FORMAT_DATETIME('%m', PARSE_DATE('%m', CAST(month AS STRING))) as month,
     row_number() over(partition by genus, year) as rn
 FROM `bigquery-public-data.gbif.occurrences`
 WHERE class='Aves'