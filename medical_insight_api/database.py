from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv('../.env', override=True)
DB_URL = os.getenv('POSTGRES_URL')

engine = create_engine(DB_URL)
session_local = sessionmaker(bind=engine)