with recursive date_series as (
    select date('2024-01-01') as date
    union all
    select date_add(date, interval 1 day)
    from date_series
    where date < '2025-12-31'
)

select
    date
from date_series
