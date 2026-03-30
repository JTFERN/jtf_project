{% macro str_null(column) %}

    COALESCE(NULLIF(TRIM({{ column }}), ''), '--')
    
{% endmacro %}