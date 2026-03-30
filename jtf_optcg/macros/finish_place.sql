{% macro place_norm(column) %}

    {% if target.type == 'bigquery' %}
        CASE 
            WHEN SAFE_CAST(REGEXP_EXTRACT({{ column }}, r'(\d+)') AS {{ dbt.type_int() }}) = 1                THEN '1st'
            WHEN SAFE_CAST(REGEXP_EXTRACT({{ column }}, r'(\d+)') AS {{ dbt.type_int() }}) = 2                THEN '2nd'
            WHEN SAFE_CAST(REGEXP_EXTRACT({{ column }}, r'(\d+)') AS {{ dbt.type_int() }}) BETWEEN 3  AND 4   THEN 'T4'
            WHEN SAFE_CAST(REGEXP_EXTRACT({{ column }}, r'(\d+)') AS {{ dbt.type_int() }}) BETWEEN 5  AND 8   THEN 'T8'
            WHEN SAFE_CAST(REGEXP_EXTRACT({{ column }}, r'(\d+)') AS {{ dbt.type_int() }}) BETWEEN 9  AND 16  THEN 'T16'
            WHEN SAFE_CAST(REGEXP_EXTRACT({{ column }}, r'(\d+)') AS {{ dbt.type_int() }}) BETWEEN 17 AND 32  THEN 'T32'
            WHEN SAFE_CAST(REGEXP_EXTRACT({{ column }}, r'(\d+)') AS {{ dbt.type_int() }}) BETWEEN 33 AND 64  THEN 'T64'
            WHEN SAFE_CAST(REGEXP_EXTRACT({{ column }}, r'(\d+)') AS {{ dbt.type_int() }}) > 64               THEN 'T++'
            ELSE '--'
        END
    {% else %}
        CASE 
            WHEN TRY_CAST(regexp_extract({{ column }}, '(\d+)', 1) AS {{ dbt.type_int() }}) = 1                THEN '1st'
            WHEN TRY_CAST(regexp_extract({{ column }}, '(\d+)', 1) AS {{ dbt.type_int() }}) = 2                THEN '2nd'
            WHEN TRY_CAST(regexp_extract({{ column }}, '(\d+)', 1) AS {{ dbt.type_int() }}) BETWEEN 3  AND 4   THEN 'T4'
            WHEN TRY_CAST(regexp_extract({{ column }}, '(\d+)', 1) AS {{ dbt.type_int() }}) BETWEEN 5  AND 8   THEN 'T8'
            WHEN TRY_CAST(regexp_extract({{ column }}, '(\d+)', 1) AS {{ dbt.type_int() }}) BETWEEN 9  AND 16  THEN 'T16'
            WHEN TRY_CAST(regexp_extract({{ column }}, '(\d+)', 1) AS {{ dbt.type_int() }}) BETWEEN 17 AND 32  THEN 'T32'
            WHEN TRY_CAST(regexp_extract({{ column }}, '(\d+)', 1) AS {{ dbt.type_int() }}) BETWEEN 33 AND 64  THEN 'T64'
            WHEN TRY_CAST(regexp_extract({{ column }}, '(\d+)', 1) AS {{ dbt.type_int() }}) > 64               THEN 'T++'
            ELSE '--'
        END
    {% endif %}
    
{% endmacro %}