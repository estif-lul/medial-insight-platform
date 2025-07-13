CREATE TABLE IF NOT EXISTS raw_telegram_messages (
    id SERIAL PRIMARY KEY,
    message_id TEXT UNIQUE,
    date TIMESTAMP,
    message TEXT NULL,
    has_image BOOLEAN NULL,
    channel_name TEXT
);

CREATE TABLE fct_image_detections (
    detection_id SERIAL PRIMARY KEY,
    message_id TEXT REFERENCES raw_telegram_messages(message_id),
    detected_object_class TEXT,
    confidence_score FLOAT,
    channel_name TEXT
);