import yfinance as yf
from inference.predict import load_model, predict_next
from trading.signal import generate_signal
from trading.risk import apply_risk
from trading.broker_api import order_market_buy, order_market_sell

def auto_trade(token, ticker="005930.KS", window=20):
    df = yf.download(ticker, period="2d", interval="5m")
    recent = df["Close"].values[-window:]

    model = load_model()
    pred = predict_next(model, recent)

    signal = generate_signal(pred)
    action = apply_risk(signal, current_position=0)

    print("Signal:", signal, "→ Action:", action)

    if action == "BUY":
        return order_market_buy(token, code="005930", qty=1)
    if action == "SELL":
        return order_market_sell(token, code="005930", qty=1)
    return {"msg": "HOLD"}
