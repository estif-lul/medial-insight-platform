SELECT DISTINCT
    channel_name AS channel_id,
    AVG(LENGTH(text)) AS avg_message_length,
    AVG(CASE WHEN has_image THEN 1 ELSE 0 END) AS image_ratio,
    MIN(message_date) AS first_seen,
    MAX(message_date) AS last_seen
FROM {{ ref('stg_telegram_messages') }}
GROUP BY channel_name