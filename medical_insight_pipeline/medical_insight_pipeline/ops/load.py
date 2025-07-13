from dagster import op

import sys, os
sys.path.insert(1, '../src')
from load import PostgresLoader


@op
def load_raw_to_postgres(scraped_data):
    channel_name = 'CheMed123'
    
    data_dir = 'data/raw/telegram_messages'
    latest_data = os.listdir(data_dir)
    latest_data.sort(reverse=True)
    print(latest_data[0])

    loader = PostgresLoader(channel_name=channel_name)
    loader.load_json(f'{data_dir}/{latest_data[0]}/@{channel_name}.json')