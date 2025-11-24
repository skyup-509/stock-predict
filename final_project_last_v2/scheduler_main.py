# scheduler.py

import time
import datetime
from main import run_train, run_auto_trade
from trading.broker_api import get_token
import warnings
warnings.filterwarnings('ignore')

# 1분마다 자동 매매
TRADE_INTERVAL = 60          # 1분
# 10분마다 학습
TRAIN_INTERVAL = 600         # 10분

last_trade = 0
last_train = 0

while True:
    now = time.time()

    # 🔹 자동 매매 (1분마다)
    if now - last_trade >= TRADE_INTERVAL:
        print("\n=== 자동 매매 실행 ===")
        try:
            token = get_token()
            run_auto_trade(token)
        except Exception as e:
            print("자동 매매 오류:", e)
        last_trade = now

    # 🔹 모델 학습 (10분마다)
    if now - last_train >= TRAIN_INTERVAL:
        print("\n=== 모델 학습 실행 ===")
        try:
            run_train()
        except Exception as e:
            print("훈련 오류:", e)
        last_train = now

    # 1초 sleep
    time.sleep(1)
