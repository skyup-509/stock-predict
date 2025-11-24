import yfinance as yf
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import ta
from sklearn.preprocessing import MinMaxScaler

def load_data(ticker):
    df = yf.download(ticker, interval="5m", period="60d")

    # MultiIndex 제거
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.dropna()

    # 모든 컬럼 1D 보장
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if isinstance(df[col], pd.DataFrame):
            df[col] = df[col].iloc[:, 0]
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()
    return df


def add_features_and_delta(df, k=1):
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
    df["atr"] = ta.volatility.AverageTrueRange(high, low, close, 14).average_true_range()
    df["roc"] = ta.momentum.ROCIndicator(close).roc()
    df["log_return"] = np.log(close / close.shift(1))
    df["vol_chg"] = vol.pct_change()

    df["future"] = df["Close"].shift(-k)
    df["delta"] = df["future"] - df["Close"]

    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    return df


class PriceDataset(Dataset):
    def __init__(self, df, window=60):
        self.window = window
        self.features = [
            "Close","rsi","ema20","ema60","macd","macd_signal",
            "atr","roc","log_return","vol_chg"
        ]

        self.feature_scaler = MinMaxScaler()
        X_scaled = self.feature_scaler.fit_transform(df[self.features])

        self.delta_scaler = MinMaxScaler()
        y_scaled = self.delta_scaler.fit_transform(df["delta"].values.reshape(-1, 1))

        X, y = [], []
        for i in range(len(df) - window):
            X.append(X_scaled[i:i+window])
            y.append(y_scaled[i+window])

        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


def get_loader(df, window=60, batch=64):
    dataset = PriceDataset(df, window)

    train_size = int(len(dataset) * 0.8)
    test_size = len(dataset) - train_size

    train_set, test_set = torch.utils.data.random_split(dataset, [train_size, test_size])

    train_loader = DataLoader(train_set, batch_size=batch, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=batch, shuffle=False)

    return (
        train_loader,
        test_loader,
        dataset.feature_scaler,
        dataset.delta_scaler,
        len(dataset.features)
    )
