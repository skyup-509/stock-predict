from core.preprocess import load_and_preprocess
from core.dataset import create_dataset
from core.predictor import load_model, predict_delta
from kis.token import get_token
from kis.order import order_market_buy
import numpy as np

# 데이터 최신
df = load_and_preprocess()
df["future"] = df["Close"].shift(-1)
df["delta"] = df["future"] - df["Close"]
df = df.dropna()

# 모델 로드
model, fscaler, dscaler = load_model()

# 마지막 window 1개로 예측
from core.dataset import create_dataset
dataset, _, _ = create_dataset(df)
X, y = dataset[-1]
X = X.unsqueeze(0)

pred = predict_delta(model, X)
delta = dscaler.inverse_transform(pred)[0][0]

print("Predicted ΔPrice:", delta)

# 방향 조건
if delta > 0:
    print("→ 매수 시도")
    token = get_token()
    print(order_market_buy(token))
else:
    print("매수 조건 아님")