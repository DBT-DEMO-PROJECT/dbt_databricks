{% macro generate_schema_name(custom_schema_name, node) %}
  {%- set target_schema = target.schema -%}

  {%- if target.name == 'bronze' and custom_schema_name == 'silver' -%}
    {{ 'silver' }}  {# In production, use only 'silver' schema #}
  {%- elif target.name == 'bronze' and custom_schema_name == 'gold' -%}
    {{ 'gold' }}  {# In production, use only 'gold' schema #}
  {%- elif custom_schema_name == 'silver' -%}
    {{ target_schema }}_silver  {# In non-production environments, combine target schema with 'silver' #}
  {%- elif custom_schema_name == 'gold' -%}  
    {{ target_schema }}_gold  {# In non-production environments, combine target schema with 'gold' #}
  {%- elif custom_schema_name is not none -%}
    {{ target_schema }}_{{ custom_schema_name | trim }}
  {%- else -%}
    {{ target_schema }}
  {%- endif -%}
{% endmacro %}
