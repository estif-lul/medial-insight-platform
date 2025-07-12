CREATE TABLE IF NOT EXISTS raw_telegram_messages (
    id SERIAL PRIMARY KEY,
    message_id INTEGER,
    date TIMESTAMP,
    message TEXT NULL,
    has_image BOOLEAN NULL,
    channel_name TEXT
);