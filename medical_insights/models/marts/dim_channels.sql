with messages as (

    select * from {{ ref('stg_telegram_messages') }}

)

select distinct
    -- Extract channel name from media path or a fixed name
    '{{ var("channel_name", "lobelia4cosmetics") }}' as channel_name,
    -- You can add more metadata later (like URL, if available)
    '{{ var("channel_url", "https://t.me/lobelia4cosmetics") }}' as channel_url

from messages
