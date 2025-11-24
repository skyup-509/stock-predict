# trading/risk.py

def apply_risk(signal: str, current_position: int) -> str:
    """
    포지션 0: BUY만 허용
    포지션 1: SELL만 허용
    """
    if signal == "BUY" and current_position == 0:
        return "BUY"
    if signal == "SELL" and current_position == 1:
        return "SELL"
    return "HOLD"
