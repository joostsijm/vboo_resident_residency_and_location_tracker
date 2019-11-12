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

# scheduler
scheduler = BackgroundScheduler()
scheduler.start()

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
# create file handler which logs even debug messages
FILE_HANDLER = logging.FileHandler('irlt.log')
FILE_HANDLER.setLevel(logging.INFO)
# create console handler with a higher log level
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(logging.INFO)
# create formatter and add it to the handlers
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
STREAM_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setFormatter(FORMATTER)
# add the handlers to logger
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)

# api
BASE_URL = os.environ["API_URL"]
HEADERS = {
    'Authorization': os.environ["AUTHORIZATION"]
}
