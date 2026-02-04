import os 
import logging
from dotenv import load_dotenv
load_dotenv(.env)

DB_HOST = os.getenv("DB_HOST")
DB_PORT= os.getenv("DB_PORT")
DB_NAME= os.getenv("DB_NAME")
DB_PASSWORD= os.get("DB_PASS")
DB_USER= os.getenv ("DB_USER")
APP_VERSION = os.getenv("APP_VERSION")