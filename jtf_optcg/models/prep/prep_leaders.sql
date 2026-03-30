with base as (
select
        name_set,
        {% if target.type == 'bigquery' %}
                regexp_extract(name_set, r'^(.+?)(?:OP|ST|P-|EB|PRB)') as leader_name,
                regexp_extract(name_set, r'^.+?((?:OP|ST|P-|EB|PRB).+)$') as leader_id,
        {% else %}
                regexp_extract(name_set, '^(.+?)(OP|ST|P-|EB|PRB)', 1) as leader_name,
                regexp_extract(name_set, '^.+?((OP|ST|P-|EB|PRB).+)$', 1) as leader_id,
        {% endif %}
        color,
        case when color like '%/%' then 2 else 1 end as color_numbers,
        {% if target.type == 'bigquery' %}
                regexp_extract(color, r'^([^/]+)') as primary_color,
                regexp_extract(color, r'/(.+)$')   as secondary_color,
        {% else %}
                regexp_extract(color, '^([^/]+)', 1) as primary_color,
                regexp_extract(color, '/(.+)$', 1)   as secondary_color,
        {% endif %}

        life,
        power

from {{ ref ('stg_leaders') }}
)

select
        leader_name,
        leader_id,
        color,
        color_numbers,
        {{str_null ('primary_color')}} as primary_color,
        {{str_null ('secondary_color')}} as secondary_color,
        life,
        power
from base