import torch
import pickle
import numpy as np
from models.lstm_delta import DeltaLSTM

def load_model(model_dir="models/"):
    feature_scaler = pickle.load(open(model_dir + "feature_scaler.pkl", "rb"))
    delta_scaler = pickle.load(open(model_dir + "delta_scaler.pkl", "rb"))

    sample_input_size = len(feature_scaler.feature_range)
    model = DeltaLSTM(input_size=10)
    model.load_state_dict(torch.load(model_dir + "model.pth"))
    model.eval()

    return model, feature_scaler, delta_scaler


def predict_delta(model, X):
    with torch.no_grad():
        pred = model(X).numpy()
    return pred