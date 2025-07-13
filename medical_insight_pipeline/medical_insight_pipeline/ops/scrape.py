from dagster import op
import asyncio
import sys, os
sys.path.insert(1, '../src')
print(os.path.dirname(os.path.abspath(__file__)))
from scrapper import main

@op
def scrape_telegram_data():
    asyncio.run(main())
    return "Scrapped data"
