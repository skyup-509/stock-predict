# trading/automator.py

import yfinance as yf
import pandas as pd

from datasets.preprocessing import add_features_and_delta
from inference.predict import load_model, predict_next

from trading.position_manager import (
    get_position, append_buy, append_sell
)

from trading.broker_api import order_market_buy, order_market_sell


def auto_trade(token, ticker="005930.KS", window=60):
    pos = get_position("005930")
    qty = pos["qty"]
    entry_price = pos["avg_price"]

    # 1) 데이터 로드
    df = yf.download(ticker, period="2d", interval="5m")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.dropna()

    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if isinstance(df[col], pd.DataFrame):
            df[col] = df[col].iloc[:, 0]

    # 2) 피처 생성
    df = add_features_and_delta(df)

    # 3) 모델 불러오기
    model, fscaler, dscaler = load_model()

    # 4) 예측
    pred_price, delta = predict_next(model, df, fscaler, dscaler, window)
    current_price = float(df["Close"].iloc[-1])

    print("\n===== AUTO TRADE =====")
    print(f"현재가: {current_price}")
    print(f"평단가: {entry_price}")
    print(f"예측가: {pred_price:.2f}   Δ {delta:+.4f}")
    print(f"보유수량: {qty}")

    # ===========================
    # 5) 매수 조건 (원하면 바꿀 수 있음)
    # ===========================
    if qty == 0:  # 보유 없을 때만 매수
        if pred_price > current_price:
            print("매수 조건 충족 → BUY!")

            # 브로커 API 실행
            res = order_market_buy(token, code="005930", qty=1)

            # JSON 포지션 업데이트
            append_buy("005930", current_price, 1)

            return res

        print("보유 없음 → 매수 조건 미충족 → HOLD")
        return {"msg": "HOLD"}

    # ===========================
    # 6) 매도 조건
    # ===========================
    if qty > 0:
        if pred_price > entry_price:  # 평단보다 예측가가 높음
            print("매도 조건 충족 → SELL!")

            pnl = current_price - entry_price
            ror = pnl / entry_price * 100
            print(f"손익: {pnl:+.0f}원 ({ror:+.2f}%)")

            res = order_market_sell(token, code="005930", qty=qty)

            append_sell("005930", qty)

            return res

        print("예측가 < 평단 → HOLD")
        return {"msg": "HOLD"}

    print("기타 HOLD")
    return {"msg": "HOLD"}
