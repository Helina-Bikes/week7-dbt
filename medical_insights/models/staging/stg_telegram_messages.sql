
WITH raw AS (

    SELECT * FROM {{ source('telegram_raw', 'raw_telegram_messages') }}

)

select
    cast(message_id as int) as message_id,
    cast(message_date as timestamp) as message_date,
    message as message_text,
    channel_name,
    channel_url,
    has_media,
    media_type,
    media_file_name
FROM raw