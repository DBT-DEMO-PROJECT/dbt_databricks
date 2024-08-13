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

-- Main query to calculate average billable percentage and select top 10 employees
select
  u.employee_id,
  u.employee_name,
  u.total_hours,
  round(avg(ru.utilization_percentage), 2) as average_billable_percentage
from utilization u
join {{ ref('stg_resource_utilization') }} ru 
  on u.employee_id = ru.employee_id
group by u.employee_id, u.employee_name, u.total_hours
order by u.total_hours desc
limit 10
