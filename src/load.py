from dotenv import load_dotenv
import os

import jsonschema.exceptions
from sqlalchemy import create_engine
from psycopg2.extras import execute_batch
import jsonschema, json, logging
from schema import message_schema

load_dotenv('.env', override=True)
DB_URL = os.getenv('POSTGRES_URL')

class PostgresLoader:
    def __init__(self, db_url, channel_name):
        self.engine = create_engine(db_url)
        self.channel_name = channel_name
        logging.basicConfig(filename='logs/loader.log', level=logging.INFO)

    def validate(self, record):
        try:
            jsonschema.validate(instance=record, schema=message_schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            logging.warning(f'Validation failed: {e.message}')
            return False
        

    def load_json(self, filepath):
        with open(filepath) as f:
            data = json.load(f)

        valid_records = [(
            f'{self.channel_name}_{r['id']}', r['date'], r.get('message', ''), 'photo' in r.get('media', {}), self.channel_name
        ) for r in data]

        # print(valid_records)

        with self.engine.connect() as nr_conn:
            conn = nr_conn.connection
            cursor = conn.cursor()
            try:
                execute_batch(cursor, """
                    INSERT INTO raw_telegram_messages (message_id, date, message, has_image, channel_name)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (message_id) DO NOTHING
                """, valid_records)
                conn.commit()
                logging.info(f'Inserted {len(valid_records)} records from {filepath}')
            except Exception as e:
                logging.error(f'Insert failed: {e}')
                print(e)
                conn.rollback()


if __name__ == '__main__':
    channel_name = 'CheMed123'
    
    data_dir = 'data/raw/telegram_messages'
    latest_data = os.listdir(data_dir)
    latest_data.sort(reverse=True)
    print(latest_data[0])

    loader = PostgresLoader(DB_URL, channel_name)
    loader.load_json(f'{data_dir}/{latest_data[0]}/@{channel_name}.json')

