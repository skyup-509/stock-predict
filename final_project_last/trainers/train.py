# trainers/train.py

import torch
from torch import nn, optim
from configs.config import EPOCHS, LR, MODEL_PATH
import os

def train(model, loader, device="cpu"):
    model.train()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)

    for epoch in range(1, EPOCHS+1):
        total_loss = 0
        for X, y in loader:
            X, y = X.to(device), y.to(device)

            pred = model(X).squeeze()
            loss = criterion(pred, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"[{epoch}/{EPOCHS}] Loss: {total_loss/len(loader):.6f}")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)
    print("Model saved.")
