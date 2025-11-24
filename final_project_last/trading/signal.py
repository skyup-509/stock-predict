def generate_signal(pred_delta):
    if pred_delta > 0:
        return "BUY"
    elif pred_delta < 0:
        return "SELL"
    return "HOLD"
