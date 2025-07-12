SELECT DISTINCT
    channel_name AS channel_id,
    MIN(message_date) AS first_seen
FROM {{ ref('stg_telegram_messages') }}
GROUP BY channel_name