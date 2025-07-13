from telethon import TelegramClient
from telethon import errors
import os
from dotenv import load_dotenv
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import asyncio

# Load environment variables once
load_dotenv('.env', override=True)
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

async def scrape_channel(channel_username, media_dir):
    """
    Asynchronously scrapes messages and media from a specified Telegram channel.
    Connects to the Telegram API using the provided channel username, downloads all messages (including media such as photos),
    and saves the messages as a JSON file in a structured directory. Media files are saved to the specified media directory.
    A progress bar is displayed during the scraping process.
    Args:
        channel_username (str): The username or ID of the Telegram channel to scrape.
        media_dir (str): The directory path where downloaded media files will be saved.
    Raises:
        telethon.errors.FloodWaitError: If the Telegram API rate limits the requests.
    Side Effects:
        - Downloads media files to the specified directory.
        - Writes a JSON file containing all scraped messages to the data/raw/telegram_messages directory.
    """

    try:
        client = TelegramClient(f'session_{channel_username}', api_id, api_hash)
        await client.start()
        entity = await client.get_entity(channel_username)
        channel_title = entity.title
        print(f"Scrapping data from {channel_title}")

        total = await client.get_messages(entity, limit=0)
        total_count = total.total if hasattr(total, 'total') else 10000

        pbar = tqdm(total=total_count, desc=f"Scraping {channel_title}", unit='message')

        messages = []
        # print('here!')

        async for message in client.iter_messages(entity, limit=total_count):
            if message.media and hasattr(message.media, 'photo'):
                filename = f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, media_path)

            msg_dict = message.to_dict()
            msg_dict = convert_datetime(msg_dict)
            messages.append(
                msg_dict
            )

            pbar.update(1)

        date_str = datetime.now().strftime("%Y-%m-%d")
        path = f'data/raw/telegram_messages/{date_str}/{channel_username}.json'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(messages, f, indent=4)


        pbar.close()
        await client.disconnect()
    except errors.FloodWaitError as e:
        print(f'An error occures:  {e}')

def run_scraper(channel_username, media_dir):
    import asyncio
    asyncio.run(scrape_channel(channel_username, media_dir))

def convert_datetime(obj):
    if isinstance(obj, dict):
        return {k: convert_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime(i) for i in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        return obj.hex()  # or use base64 if you prefer
    else:
        return obj

async def main():
    media_dir = 'data/raw/photos'
    os.makedirs(media_dir, exist_ok=True)
    channels = [
            '@lobelia4cosmetics' 
        ]
    await scrape_channel(channels[0], media_dir)

    # with ThreadPoolExecutor(max_workers=3) as executor:
    #     for channel in channels:
    #         executor.submit(run_scraper, channel, media_dir)

if __name__ == "__main__":
    asyncio.run(main())