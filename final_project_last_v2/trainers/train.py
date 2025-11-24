import torch
from torch import nn, optim
from configs.config import EPOCHS, LR, MODEL_PATH
import os

def train(model, train_loader, feature_scaler, delta_scaler, input_size, device="cpu"):
    model.train()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)

    for epoch in range(1, EPOCHS+1):
        loss_sum = 0

        for X, y in train_loader:
            X, y = X.to(device), y.to(device)

            pred = model(X)
            loss = criterion(pred, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            loss_sum += loss.item()

        print(f"[{epoch}/{EPOCHS}] Loss: {loss_sum / len(train_loader):.6f}")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    torch.save({
        "model": model.state_dict(),
        "feature_scaler": feature_scaler,
        "delta_scaler": delta_scaler,
        "input_size": input_size
    }, MODEL_PATH)

    print("Model saved.")
