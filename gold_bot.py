import requests
import os
import jdatetime

API_KEY = os.environ["GOLD_API_KEY"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = "@goldentrend_online"   # یوزرنیم کانال خودت رو اینجا بذار

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}

def get_prices():
    url = f"https://BrsApi.ir/Api/Market/Gold_Currency.php?key={API_KEY}"
    data = requests.get(url, headers=HEADERS).json()

    gold_18k = next(item for item in data["gold"] if item["symbol"] == "IR_GOLD_18K")
    gold_ounce = next(item for item in data["gold"] if item["symbol"] == "XAUUSD")
    tether = next(item for item in data["currency"] if item["symbol"] == "USDT_IRT")

    return gold_18k, gold_ounce, tether

def send_to_channel(gold_18k, gold_ounce, tether):
    now = jdatetime.datetime.now()
    date_str = now.strftime("%Y/%m/%d")
    time_str = now.strftime("%H:%M")

    tether_price = int(float(tether["price"]))

    text = (
        f"💰 قیمت‌های لحظه‌ای\n\n"
        f"🔸 مظنه (انس جهانی): {gold_ounce['price']} دلار\n"
        f"🔸 طلای ۱۸ عیار: {gold_18k['price']:,} تومان\n"
        f"🔸 تتر: {tether_price:,} تومان\n\n"
        f"🗓 تاریخ: {date_str} | ⏰ ساعت: {time_str}\n"
        f"📢 {CHANNEL_ID}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHANNEL_ID, "text": text})


if __name__ == "__main__":
    gold_18k, gold_ounce, tether = get_prices()
    send_to_channel(gold_18k, gold_ounce, tether)
