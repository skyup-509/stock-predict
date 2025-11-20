import yfinance as yf
import pandas as pd
import numpy as np
import ta

def load_and_preprocess(ticker="005930.KS", period="60d", interval="5m"):
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=True)
    df = df.dropna()

    # MultiIndex 제거
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]

    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()

    # 기술지표
    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    vol = df["Volume"]

    df["rsi"] = ta.momentum.RSIIndicator(close, 14).rsi()
    df["ema20"] = ta.trend.EMAIndicator(close, 20).ema_indicator()
    df["ema60"] = ta.trend.EMAIndicator(close, 60).ema_indicator()
    macd = ta.trend.MACD(close)
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["atr"] = ta.volatility.AverageTrueRange(high, low, close, 5).average_true_range()
    df["roc"] = ta.momentum.ROCIndicator(close).roc()
    df["log_return"] = np.log(close / close.shift(1))
    df["vol_chg"] = vol.pct_change()

    df = df.replace([np.inf, -np.inf], np.nan).dropna()

    return df