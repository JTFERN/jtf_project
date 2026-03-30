with source as (

    select * from {{ source('raw', 'decklists') }}

),

renamed as (

    select
        {% if target.type == 'bigquery' %}
            deck_profile,
            deck_name,
            coalesce(
                safe.parse_date('%m/%d/%Y', date),
                safe.parse_date('%b %d, %Y', date)
            ) as finish_dt,
        {% else %}
            "deck profile" as deck_profile,
            "deck name" as deck_name,
            coalesce(
                try_strptime(date, '%m/%d/%Y'),
                try_strptime(date, '%b %d, %Y')
            )::DATE as finish_dt,
        {% endif %}
        cast(country as {{ dbt.type_string() }}) as country,
        cast(author as {{ dbt.type_string() }}) as author,
        cast(placement as {{ dbt.type_string() }}) as placement,
        cast(tournament as {{ dbt.type_string() }}) as tournament,
        cast(host as {{ dbt.type_string() }}) as host,
        cast(leader_id as {{ dbt.type_string() }}) as leader_id,
        cast(set_name as {{ dbt.type_string() }}) as set_name

    from source

)

select * from renamed