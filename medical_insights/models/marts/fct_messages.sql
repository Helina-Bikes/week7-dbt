with messages as (

    select * from {{ ref('stg_telegram_messages') }}

),
channels as (

    select * from {{ ref('dim_channels') }}

),
dates as (

    select * from {{ ref('dim_dates') }}

)

select
    m.message_id,
    m.message_text,
    d.date as message_date,
    c.channel_name
  

from messages m
left join channels c on c.channel_name = '{{ var("channel_name", "lobelia4cosmetics") }}'
left join dates d on d.date = m.message_date
