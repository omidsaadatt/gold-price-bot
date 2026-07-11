import requests
import os
import jdatetime

API_KEY = os.environ["GOLD_API_KEY"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = "@goldentrend_online"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}

def get_prices():
    url = f"https://BrsApi.ir/Api/Market/Gold_Currency.php?key={API_KEY}"
    data = requests.get(url, headers=HEADERS).json()

    gold_18k = next(item for item in data["gold"] if item["symbol"] == "IR_GOLD_18K")
    gold_melted = next(item for item in data["gold"] if item["symbol"] == "IR_GOLD_MELTED")
    gold_ounce = next(item for item in data["gold"] if item["symbol"] == "XAUUSD")
    coin_emami = next(item for item in data["gold"] if item["symbol"] == "IR_COIN_EMAMI")
    tether = next(item for item in data["currency"] if item["symbol"] == "USDT_IRT")
    usd = next(item for item in data["currency"] if item["symbol"] == "USD")

    return gold_18k, gold_melted, gold_ounce, coin_emami, tether, usd

def calculate_bubble(gold_18k_price, ounce_price, usd_price):
    fair_24k_gram = (ounce_price * usd_price) / 31.1
    fair_18k_gram = fair_24k_gram * 0.75
    bubble_amount = gold_18k_price - fair_18k_gram
    bubble_percent = (gold_18k_price / fair_18k_gram - 1) * 
