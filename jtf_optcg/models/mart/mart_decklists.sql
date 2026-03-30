select
    d.deck_name,
    d.finish_dt,
    d.placement,
    d.tournament,
    d.host,
    d.set_name,
    d.leader_id,
    l.leader_name,
    l.color,
    l.color_numbers,
    l.primary_color,
    l.secondary_color,
    l.life,
    l.power
from {{ref ('prep_decklists')}} as d
inner join {{ ref ('prep_leaders')}} as l
    on d.leader_id=l.leader_id