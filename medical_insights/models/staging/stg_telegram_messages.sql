WITH raw AS (

    SELECT * FROM {{ source('telegram_raw', 'raw_telegram_messages') }}

)

SELECT
    message_id,
    message AS message_text,
    STR_TO_DATE(message_date, '%Y-%m-%d %H:%i:%s') AS message_date,
    channel_name,
    channel_url

FROM raw
