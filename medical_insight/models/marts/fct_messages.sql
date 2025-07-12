SELECT
    msg.message_id,
    msg.message_date,
    ch.channel_id,
    msg.message,
    msg.has_image
FROM {{ ref('stg_telegram_messages') }} msg
JOIN {{ ref('dim_channels') }} ch
ON msg.channel_name = ch.channel_id