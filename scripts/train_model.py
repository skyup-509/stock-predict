import json
import requests
from .config import APP_KEY, APP_SECRET, ACCOUNT, ACCOUNT_TYPE

def order_market_buy(token, code="005930", qty=1):
    url = "https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/trading/order-cash"

    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "VTTC0802U"
    }

    body = {
        "CANO": ACCOUNT,
        "ACNT_PRDT_CD": ACCOUNT_TYPE,
        "PDNO": code,
        "ORD_DVSN": "01",
        "ORD_QTY": str(qty),
        "ORD_UNPR": "0"
    }

    r = requests.post(url, headers=headers, data=json.dumps(body))
    return r.json()