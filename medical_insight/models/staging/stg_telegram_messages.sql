SELECT
    message_id,
    CAST(date AS TIMESTAMP) AS message_date,
    channel_name,
    message,
    CASE WHEN has_image THEN TRUE ELSE FALSE END AS has_image
FROM public.raw_telegram_messages