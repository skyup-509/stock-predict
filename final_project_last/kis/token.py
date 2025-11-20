import json
import requests
from .config import APP_KEY, APP_SECRET

def get_token():
    url = "https://openapi.koreainvestment.com:9443/oauth2/tokenP"

    data = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET
    }

    res = requests.post(url, data=json.dumps(data))
    return res.json().get("access_token", None)