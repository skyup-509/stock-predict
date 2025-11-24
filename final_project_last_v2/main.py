import torch
from datasets.preprocessing import load_data, add_features_and_delta, get_loader
from models.lstm_model import LSTMModel
from trainers.train import train
from trading.automator import auto_trade
from configs.config import TICKER, WINDOW
from trading.broker_api import get_token
import warnings
warnings.filterwarnings('ignore')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def run_train():
    print("Loading data...")
    df = load_data(TICKER)
    df = add_features_and_delta(df)

    train_loader, test_loader, feature_scaler, delta_scaler, input_size = get_loader(df, WINDOW)

    model = LSTMModel(input_size=input_size).to(device)
    print("Training...")
    train(model, train_loader, feature_scaler, delta_scaler, input_size, device)

def run_auto_trade():
    token = get_token()
    auto_trade(token)

if __name__ == "__main__":
    mode = input("1: Train, 2: AutoTrade → ")

    if mode == "1":
        run_train()
    else:
        run_auto_trade()
