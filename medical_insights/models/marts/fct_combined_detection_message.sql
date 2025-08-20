-- fct_combined_detection_message.sql

with messages as (
  select
    message_id,
    message_date,
    channel_name,
    media_file_name
  from {{ ref('stg_telegram_messages') }}
),

detections as (
  select
    detection_id,
    detected_object_class,
    confidence_score,
    media_file_name
  from {{ ref('stg_image_detections') }}
)

select
  d.detection_id,
  m.message_id,
  m.message_date,
  m.channel_name,
  d.detected_object_class,
  d.confidence_score
from detections d
left join messages m
  on d.media_file_name = m.media_file_name
