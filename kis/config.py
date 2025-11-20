import os
from dotenv import load_dotenv

load_dotenv()

APP_KEY = os.getenv("KIS_API_KEY")
APP_SECRET = os.getenv("KIS_API_SECRET")
ACCOUNT = os.getenv("KIS_ACCOUNT")
ACCOUNT_TYPE = "01"