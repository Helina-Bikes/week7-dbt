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
    cast(m.message_date as date) as message_date,
    c.channel_name,
    m.has_media,
    m.media_type,
    m.media_file_name,
    length(m.message_text) as message_length
from
    messages m
    left join channels c on m.channel_name = c.channel_name
    left join dates d on d.date = cast(m.message_date as date)