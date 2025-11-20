import numpy as np
import torch
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import TensorDataset

def create_dataset(df, lookback=60):
    features = [
        "Close","rsi","ema20","ema60","macd","macd_signal",
        "atr","roc","log_return","vol_chg"
    ]

    # 스케일러
    feature_scaler = MinMaxScaler()
    scaled_features = feature_scaler.fit_transform(df[features])

    # delta (future-close)
    delta_scaler = MinMaxScaler()
    delta_scaled = delta_scaler.fit_transform(df["delta"].values.reshape(-1, 1))

    X, y = [], []
    for i in range(len(df) - lookback):
        X.append(scaled_features[i:i+lookback])
        y.append(delta_scaled[i+lookback])

    X = torch.tensor(np.array(X), dtype=torch.float32)
    y = torch.tensor(np.array(y), dtype=torch.float32)

    dataset = TensorDataset(X, y)

    return dataset, feature_scaler, delta_scaler