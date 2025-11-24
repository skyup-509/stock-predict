import torch
import numpy as np
from models.lstm_model import LSTMModel
from configs.config import MODEL_PATH
from sklearn.preprocessing import MinMaxScaler
import torch.serialization

torch.serialization.add_safe_globals([MinMaxScaler])

def load_model(device="cpu"):
    ckpt = torch.load(MODEL_PATH, map_location=device, weights_only=False)

    model = LSTMModel(input_size=ckpt["input_size"]).to(device)
    model.load_state_dict(ckpt["model"])
    model.eval()

    return model, ckpt["feature_scaler"], ckpt["delta_scaler"]

def predict_next(model, df, feature_scaler, delta_scaler, window=60, device="cpu"):

    features = [
        "Close","rsi","ema20","ema60","macd","macd_signal",
        "atr","roc","log_return","vol_chg"
    ]

    recent = df[features].iloc[-window:].values
    recent_scaled = feature_scaler.transform(recent)

    X = torch.tensor(recent_scaled, dtype=torch.float32).unsqueeze(0).to(device)

    with torch.no_grad():
        delta_scaled = model(X).cpu().numpy()

    delta = delta_scaler.inverse_transform(delta_scaled)[0][0]
    price = df["Close"].iloc[-1] + delta

    return price, delta
