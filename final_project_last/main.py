import torch
from datasets.preprocessing import load_data, get_loader
from models.lstm_model import LSTMModel
from trainers.train import train
from trading.automator import auto_trade
from configs.config import TICKER, WINDOW
from trading.broker_api import get_token

def run_train():
    df = load_data(TICKER)
    loader = get_loader(df, WINDOW)

    model = LSTMModel()
    train(model, loader)

def run_auto_trade(token):
    result = auto_trade(token)
    print(result)

if __name__ == "__main__":
    mode = input("1: Train, 2: AutoTrade → ")

    if mode == "1":
        run_train()
    else:
        token = get_token()
        run_auto_trade(token)
