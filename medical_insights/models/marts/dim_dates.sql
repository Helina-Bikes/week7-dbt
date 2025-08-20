with recursive
    date_series as (
        select cast('2024-01-01' as date) as date
        union all
        select date + interval '1 day'
        from date_series
        where
            date < '2025-12-31'
    )

select
    date,
    extract(
        year
        from date
    ) as year,
    extract(
        month
        from date
    ) as month,
    extract(
        day
        from date
    ) as day,
    extract(
        week
        from date
    ) as week,
    to_char (date, 'Day') as day_name
from date_series