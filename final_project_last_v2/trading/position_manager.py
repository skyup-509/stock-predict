# trading/position_manager.py

import json
import os

POS_FILE = "positions.json"


def load_positions():
    if not os.path.exists(POS_FILE):
        return {}
    with open(POS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_positions(data):
    with open(POS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_position(ticker):
    positions = load_positions()
    return positions.get(ticker, {"qty": 0, "avg_price": None})


def update_position(ticker, qty, avg_price):
    positions = load_positions()
    positions[ticker] = {"qty": qty, "avg_price": avg_price}
    save_positions(positions)


def clear_position(ticker):
    positions = load_positions()
    if ticker in positions:
        del positions[ticker]
    save_positions(positions)


# 🔥 매수 기능: 수량 증가 + 평단 자동 계산
def append_buy(ticker, buy_price, buy_qty):
    pos = get_position(ticker)
    old_qty = pos["qty"]
    old_price = pos["avg_price"]

    if old_qty == 0:
        # 첫 매수 = 그대로 평균가
        new_qty = buy_qty
        new_avg = buy_price
    else:
        # 기존 평단가와 새 매수 합산
        new_qty = old_qty + buy_qty
        new_avg = (old_price * old_qty + buy_price * buy_qty) / new_qty

    update_position(ticker, new_qty, new_avg)


# 🔥 매도 기능: 수량 감소 + 0이면 포지션 제거
def append_sell(ticker, sell_qty):
    pos = get_position(ticker)
    old_qty = pos["qty"]

    if sell_qty >= old_qty:
        clear_position(ticker)
    else:
        new_qty = old_qty - sell_qty
        update_position(ticker, new_qty, pos["avg_price"])
