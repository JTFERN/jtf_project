with source as (

    select * from {{ source('raw', 'leaders') }}

),

renamed as (

    select
        cast(name as {{ dbt.type_string() }}) as name_set,
        cast(color as {{ dbt.type_string() }}) color,
        cast (life as {{ dbt.type_int() }}) as life,
        cast (power as {{ dbt.type_int() }}) as power

    from source

)

select * from renamed