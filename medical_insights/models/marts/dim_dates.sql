with date_series as (

    select
        cast('2025-07-01' as date) + interval seq day as date
    from (
        select @row := @row + 1 as seq
        from information_schema.tables t1,
             information_schema.tables t2,
             (select @row := 0) init
        limit 100
    ) as dates

)

select
    date,
    dayname(date) as day_name,
    dayofmonth(date) as day,
    monthname(date) as month,
    year(date) as year,
    week(date) as week

from date_series
