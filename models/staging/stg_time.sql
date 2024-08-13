-- models/staging/stg_time.sql
with source as (
  select * from `dbtworkshop.raw_data.time_table`
)

select
  time_id,
  date,
  day_of_week,
  month,
  quarter,
  year
from source

