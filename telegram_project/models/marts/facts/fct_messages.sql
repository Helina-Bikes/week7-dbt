WITH messages AS (
    SELECT * FROM {{ ref('stg_telegram_messages') }}
),
channels AS (
    SELECT * FROM {{ ref('dim_channels') }}
),
dates AS (
    SELECT * FROM {{ ref('dim_dates') }}
)
SELECT
    m.message_id,
    m.message_text,
    m.message_date,
    m.has_media,
    m.media_type,
    m.media_file_name,
    c.channel_name,
    c.channel_url
FROM messages m
LEFT JOIN channels c ON c.channel_name = m.channel_name
LEFT JOIN dates d ON d.date = m.message_date