with raw as (

    select * from {{ source('telegram_raw', 'raw_telegram_messages') }}

)

select
    id as message_id,
    message as message_text,
    STR_TO_DATE(date, '%Y-%m-%d %H:%i:%s') as message_date,
    has_media as has_media_flag,
    media_type

from raw
