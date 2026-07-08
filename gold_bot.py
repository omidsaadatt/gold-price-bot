import requests
import os
import jdatetime

API_KEY = os.environ["GOLD_API_KEY"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = "@my_channel"   # یوزرنیم کانال خودت رو اینجا بذار

def get_gold_prices():
    url = f"https://BrsApi.ir/Api/Market/Gold_Currency.php?key={API_KEY}"
    data = requests.get(url).json()
    ounce = next(item for item in data["gold"] if "انس" in item["name"])
    molten = next(item for item in data["gold"] if "آبشده" in item["name"])
    return ounce["price"], molten["price"]

def send_to_channel(ounce_price, molten_price):
    now = jdatetime.datetime.now()
    date_str = now.strftime("%Y/%m/%d")
    time_str = now.strftime("%H:%M")

    text = (
        f"💰 قیمت لحظه‌ای طلا\n\n"
        f"🔸 انس جهانی: {ounce_price} دلار\n"
        f"🔸 طلای آبشده: {molten_price} تومان\n\n"
        f"🗓 تاریخ: {date_str} | ⏰ ساعت: {time_str}\n"
        f"📢 {CHANNEL_ID}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHANNEL_ID, "text": text})


if __name__ == "__main__":
    ounce, molten = get_gold_prices()
    send_to_channel(ounce, molten)
