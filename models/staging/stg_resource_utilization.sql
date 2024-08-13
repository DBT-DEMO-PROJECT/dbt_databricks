-- models/staging/stg_resource_utilisation.sql
with source as (
  select * from `dbtworkshop.raw_data.resource_utilisation_table`
)

select
  resource_utilization_id,
  time_id,
  employee_id,
  project_id,
  department_id,
  utilization_hours,
  utilization_percentage,
  active
from source
