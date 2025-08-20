with messages as (
    select * from {{ ref('stg_telegram_messages') }}
)

select distinct channel_name, channel_url from messages