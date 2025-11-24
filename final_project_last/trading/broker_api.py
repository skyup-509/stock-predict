# trading/broker_api.py

import json
import requests
from configs.config import APP_KEY, APP_SECRET, ACCOUNT, ACCOUNT_TYPE, BASE_URL

def get_token():
    url = f"{BASE_URL}/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    data = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET
    }

    res = requests.post(url, data=json.dumps(data))
    return res.json().get("access_token", None)

def order_market_buy(token, code="005930", qty=1):
    url = f"{BASE_URL}/uapi/domestic-stock/v1/trading/order-cash"
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "VTTC0802U",
    }
    body = {
        "CANO": ACCOUNT,
        "ACNT_PRDT_CD": ACCOUNT_TYPE,
        "PDNO": code,
        "ORD_DVSN": "01",
        "ORD_QTY": str(qty),
        "ORD_UNPR": "0"
    }
    return requests.post(url, headers=headers, data=json.dumps(body)).json()

def order_market_sell(token, code="005930", qty=1):
    url = f"{BASE_URL}/uapi/domestic-stock/v1/trading/order-cash"
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "VTTC0801U",
    }
    body = {
        "CANO": ACCOUNT,
        "ACNT_PRDT_CD": ACCOUNT_TYPE,
        "PDNO": code,
        "ORD_DVSN": "01",
        "ORD_QTY": str(qty),
        "ORD_UNPR": "0"
    }
    return requests.post(url, headers=headers, data=json.dumps(body)).json()
