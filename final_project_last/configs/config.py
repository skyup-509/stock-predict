import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

# 🔹 한국투자증권 API
APP_KEY = os.getenv("APP_KEY", "")
APP_SECRET = os.getenv("APP_SECRET", "")
ACCOUNT = os.getenv("ACCOUNT", "")
ACCOUNT_TYPE = os.getenv("ACCOUNT_TYPE", "")  # e.g., "01"

BASE_URL = "https://openapivts.koreainvestment.com:29443"

# 🔹 모델 설정
MODEL_PATH = "./saved_models/lstm.pth"
WINDOW = 20
PRED_HORIZON = 1
LR = 0.0007
EPOCHS = 15
BATCH = 32

# 🔹 티커
TICKER = "005930.KS"