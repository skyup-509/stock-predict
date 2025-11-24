def apply_risk(signal, current_position):
    if signal == "BUY" and current_position == 0:
        return "BUY"
    if signal == "SELL" and current_position > 0:
        return "SELL"
    return "HOLD"
