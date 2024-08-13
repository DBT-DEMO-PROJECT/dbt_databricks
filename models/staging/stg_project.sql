-- models/staging/stg_project.sql
with source as (
  select * from `dbtworkshop.raw_data.project_table`
)

select
  project_id,
  project_name,
  start_date,
  end_date,
  project_manager_id,
  budget
from source

