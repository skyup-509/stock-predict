# datasets/preprocessing.py

import yfinance as yf
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
import torch

def load_data(ticker, window=20):
    df = yf.download(ticker, interval="5m", period="20d")
    df = df[["Close"]].dropna()
    df["return"] = df["Close"].pct_change().fillna(0)
    return df

class PriceDataset(Dataset):
    def __init__(self, df, window=20):
        self.X = []
        self.y = []

        values = df["Close"].values

        for i in range(len(values) - window - 1):
            self.X.append(values[i:i+window])
            self.y.append(values[i+window+1] - values[i+window])  # Δprice

        self.X = np.array(self.X)
        self.y = np.array(self.y)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return (
            torch.tensor(self.X[idx], dtype=torch.float32),
            torch.tensor(self.y[idx], dtype=torch.float32),
        )

def get_loader(df, window, batch=32):
    dataset = PriceDataset(df, window)
    return DataLoader(dataset, batch_size=batch, shuffle=True)
