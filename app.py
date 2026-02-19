import requests
import time
import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PART_NUMBER = "MFY84J/A"
ZIP_CODE = "8100001"

CHECK_INTERVAL = 20
COOLDOWN = 300

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

def check_stock():
    url = "https://www.apple.com/jp/shop/fulfillment-messages"
    params = {"parts.0": PART_NUMBER, "location": ZIP_CODE}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        data = r.json()

        stores = data.get("body", {}).get("content", {}).get("pickupMessage", {}).get("stores", [])

        for store in stores:
            if "Fukuoka" in store.get("storeName", ""):
                availability = store.get("partsAvailability", {}).get(PART_NUMBER, {})
                if availability.get("pickupAvailable") == True:
                    return True
    except:
        return False

    return False


if __name__ == "__main__":
    print("Bot started...")
    while True:
        try:
            if check_stock():
                send_telegram("🔥 iPhone 17 Pro Max 256GB White có hàng tại Apple Fukuoka!")
                time.sleep(COOLDOWN)
            else:
                time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print("ERROR:", e)
            time.sleep(10)
