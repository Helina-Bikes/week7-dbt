WITH messages AS (
    SELECT * FROM {{ ref('stg_telegram_messages') }}
)
SELECT DISTINCT
    channel_name,
    channel_url
FROM messages