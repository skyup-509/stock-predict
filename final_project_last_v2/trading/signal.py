# trading/signal.py

def generate_signal(pred_delta: float) -> str:
    """
    pred_delta > 0 : 상승 예측 → BUY
    pred_delta < 0 : 하락 예측 → SELL
    pred_delta == 0 : HOLD
    """
    if pred_delta > 0:
        return "BUY"
    elif pred_delta < 0:
        return "SELL"
    return "HOLD"
