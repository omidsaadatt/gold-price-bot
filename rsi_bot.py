import requests
import os
import json
from datetime import datetime

TWELVE_DATA_KEY = os.environ["TWELVE_DATA_KEY"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = "@goldentrend_online"

STATE_FILE = "state.json"


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"1min": "neutral", "5min": "neutral", "15min": "neutral"}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def get_1min_candles():
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": "XAU/USD",
        "interval": "1min",
        "outputsize": 260,
        "order": "ASC",
        "apikey": TWELVE_DATA_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "values" not in data:
        raise Exception(f"API Error: {data}")
    candles = [(item["datetime"], float(item["close"])) for item in data["values"]]
    return candles


def resample(candles, minutes):
    buckets = {}
    for dt_str, close in candles:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        bucket_minute = dt.minute - (dt.minute % minutes)
        bucket_key = dt.replace(minute=bucket_minute, second=0)
        buckets[bucket_key] = close
    ordered_keys = sorted(buckets.keys())
    return [buckets[k] for k in ordered_keys]


def calculate_rsi(closes, period=14):
    if len(closes) < period + 1:
        return None

    gains = []
    losses = []
    for i in range(1, period + 1):
        change = closes[i] - closes[i - 1]
        gains.append(max(change, 0))
        losses.append(max(-change, 0))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    for i in range(period + 1, len(closes)):
        change = closes[i] - closes[i - 1]
        gain = max(change, 0)
        loss = max(-change, 0)
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def send_debug_message(rsi_1min, rsi_5min, rsi_15min, last_price):
    text = (
        f"🧪 تست دیباگ RSI (نسخه‌ی موقت)\n\n"
        f"💰 آخرین قیمت XAUUSD: {last_price}\n\n"
        f"📊 RSI ۱ دقیقه: {round(rsi_1min, 2) if rsi_1min else 'نامشخص'}\n"
        f"📊 RSI ۵ دقیقه: {round(rsi_5min, 2) if rsi_5min else 'نامشخص'}\n"
        f"📊 RSI ۱۵ دقیقه: {round(rsi_15min, 2) if rsi_15min else 'نامشخص'}\n\n"
        f"📢 {CHANNEL_ID}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHANNEL_ID, "text": text})


def main():
    candles = get_1min_candles()

    closes_1min = [c[1] for c in candles]
    closes_5min = resample(candles, 5)
    closes_15min = resample(candles, 15)

    rsi_1min = calculate_rsi(closes_1min)
    rsi_5min = calculate_rsi(closes_5min)
    rsi_15min = calculate_rsi(closes_15min)

    last_price = closes_1min[-1] if closes_1min else "نامشخص"

    send_debug_message(rsi_1min, rsi_5min, rsi_15min, last_price)


if __name__ == "__main__":
    main()
