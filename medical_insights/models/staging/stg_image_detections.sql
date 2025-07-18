-- models/staging/stg_image_detections.sql

with source as (

    select
        detection_id,
        detected_object_class,
        confidence_score,
        media_file_name
   from {{ ref('fct_image_detections') }}


),

renamed as (

    select
        detection_id,
        detected_object_class,
        confidence_score,
        media_file_name
    from source

)

select * from renamed
