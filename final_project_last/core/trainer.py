import torch
from torch.utils.data import DataLoader
import pickle
import os
from models.lstm_delta import DeltaLSTM

def train_model(dataset, feature_scaler, delta_scaler, save_dir="models/", epochs=20):
    os.makedirs(save_dir, exist_ok=True)

    train_size = int(len(dataset) * 0.8)
    train_set, test_set = torch.utils.data.random_split(dataset,
        [train_size, len(dataset)-train_size])

    train_loader = DataLoader(train_set, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=64, shuffle=False)

    sample_x, _ = dataset[0]
    model = DeltaLSTM(input_size=sample_x.shape[1])
    opt = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = torch.nn.MSELoss()

    for ep in range(epochs):
        model.train()
        total = 0
        for xb, yb in train_loader:
            opt.zero_grad()
            pred = model(xb)
            loss = criterion(pred, yb)
            loss.backward()
            opt.step()
            total += loss.item()
        print(f"[{ep+1}/{epochs}] Loss: {total/len(train_loader):.6f}")

    # ---------------- 저장 ----------------
    torch.save(model.state_dict(), os.path.join(save_dir, "model.pth"))
    pickle.dump(feature_scaler, open(os.path.join(save_dir, "feature_scaler.pkl"), "wb"))
    pickle.dump(delta_scaler, open(os.path.join(save_dir, "delta_scaler.pkl"), "wb"))