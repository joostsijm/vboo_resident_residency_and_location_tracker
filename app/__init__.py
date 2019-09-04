"""Inwoner Residency en Locatie Tracker"""

import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from app.models import Base, State, Region, Player


load_dotenv()

# database
engine = create_engine(os.environ["DATABASE_URI"], client_encoding='utf8')
Session = sessionmaker(bind=engine)
session = Session()

# scheduler
scheduler = BackgroundScheduler()
scheduler.start()

logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)

# api
BASE_URL = os.environ["API_URL"]
HEADERS = {
    'Authorization': os.environ["AUTHORIZATION"]
}
