import torch
from models.lstm_model import LSTMModel
from configs.config import MODEL_PATH

def load_model(device="cpu"):
    model = LSTMModel()
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.eval()
    return model

def predict_next(model, recent_window):
    # recent_window shape: (window,)
    X = torch.tensor(recent_window, dtype=torch.float32)

    # ---- 여기서 강제로 3D로 보정 ----
    # (window,) -> (1, window) -> (1, window, 1)
    X = X.unsqueeze(0).unsqueeze(-1)

    pred = model(X).detach().numpy()[0][0]
    return pred
