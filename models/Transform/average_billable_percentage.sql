-- Create the table in the target schema
{{ config(schema='gold') }}

WITH utilization AS (
  SELECT
    ru.employee_id,
    e.employee_name,
    SUM(ru.utilization_hours) AS total_hours
  FROM {{ ref('stg_resource_utilization') }} ru
  JOIN {{ ref('stg_employee') }} e ON ru.employee_id = e.employee_id
  WHERE ru.active = TRUE
  GROUP BY ru.employee_id, e.employee_name
)

-- Main query to calculate average billable percentage and select top 10 employees
SELECT
  u.employee_id,
  u.employee_name,
  u.total_hours,
  ROUND(AVG(ru.utilization_percentage), 2) AS average_billable_percentage
FROM utilization u
JOIN {{ ref('stg_resource_utilization') }} ru 
  ON u.employee_id = ru.employee_id
GROUP BY u.employee_id, u.employee_name, u.total_hours
ORDER BY u.total_hours DESC
LIMIT 10
