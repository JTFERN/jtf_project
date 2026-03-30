select
    deck_name,
    leader_id,
    finish_dt,
    country,
    author,
    set_name,
    {{place_norm('placement')}} as placement,
    {% if target.type == 'bigquery' %}
        TRIM(REGEXP_EXTRACT(tournament, r'^([^(]+)')) as tournament,
        TRIM(REGEXP_EXTRACT(host, r'^([^(]+)')) as host,
        --upper(REGEXP_EXTRACT(set_name, r'^(.+?)(?:-deck)')) as set_name
    {% else %}
        TRIM(regexp_extract(tournament, '^([^(]+)', 1)) as tournament,
        TRIM(regexp_extract(host, '^([^(]+)', 1)) as host,
        --upper(regexp_extract(set_name, '^(.+?)(-deck)', 1)) as set_name
    {% endif %}

from {{ref('stg_decklists')}}