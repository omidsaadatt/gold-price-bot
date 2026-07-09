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
    bubble_percent = (gold_18k_price / fair_18k_gram - 1) * 100
    return round(bubble_amount), round(bubble_percent, 1)

def send_to_channel(gold_18k, gold_melted, gold_ounce, coin_emami, tether, usd):
    now = jdatetime.datetime.now()
    date_str = now.strftime("%Y/%m/%d")
    time_str = now.strftime("%H:%M")

    tether_price = int(float(tether["price"]))
    bubble_amount, bubble_percent = calculate_bubble(gold_18k["price"], gold_ounce["price"], usd["price"])
    bubble_sign = "🟢+" if bubble_amount >= 0 else "🔴"

    text = (
        f"💰 قیمت‌های لحظه‌ای\n\n"
        f"🔸 مظنه (انس جهانی): {gold_ounce['price']} دلار\n"
        f"🔸 طلای ۱۸ عیار: {gold_18k['price']:,} تومان\n"
        f"🔸 طلای آب‌شده: {gold_melted['price']:,} تومان\n"
        f"🔸 سکه امامی: {coin_emami['price']:,} تومان\n"
        f"🔸 حباب طلای ۱۸ عیار: {bubble_sign}{abs(bubble_amount):,} تومان ({bubble_percent}%)\n"
        f"🔸 تتر: {tether_price:,} تومان\n\n"
        f"🗓 تاریخ: {date_str} | ⏰ ساعت: {time_str}\n"
        f"📢 {CHANNEL_ID}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHANNEL_ID, "text": text})


if __name__ == "__main__":
    gold_18k, gold_melted, gold_ounce, coin_emami, tether, usd = get_prices()
    send_to_channel(gold_18k, gold_melted, gold_ounce, coin_emami, tether, usd)
