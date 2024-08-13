-- models/top_utilizing_employees.sql

-- Common Table Expression (CTE) to calculate total utilization hours per employee
with utilization as (
  select
    ru.employee_id,
    e.employee_name,
    sum(ru.utilization_hours) as total_hours
  from {{ ref('stg_resource_utilization') }} ru
  join {{ ref('stg_employee') }} e on ru.employee_id = e.employee_id
  where ru.active = true
  group by ru.employee_id, e.employee_name
)

-- Main query to select top 10 employees based on total utilization hours
select
  employee_id,
  employee_name,
  total_hours
from utilization
order by total_hours desc
limit 10
