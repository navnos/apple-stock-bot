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
    
    params = {
        "pl": "true",
        "parts.0": PART_NUMBER,
        "location": ZIP_CODE
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.apple.com/jp/shop/buy-iphone",
        "Accept": "application/json, text/plain, */*"
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)

        print("Status:", r.status_code)

        if "json" not in r.headers.get("Content-Type", ""):
            print("Not JSON response")
            return False

        data = r.json()

        stores = data["body"]["content"]["pickupMessage"]["stores"]

        for store in stores:
            if "福岡" in store["storeName"]:
                part = store["partsAvailability"][PART_NUMBER]
                if part["pickupDisplay"] == "available":
                    return True

    except Exception as e:
        print("ERROR:", e)

    return False

if __name__ == "__main__":
    print("Bot started...")
    while True:
        try:
            print("Checking stock...")
            if check_stock():
                send_telegram("🔥 iPhone 17 Pro Max 256GB White có hàng tại Apple Fukuoka!")
                time.sleep(COOLDOWN)
            else:
                time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print("ERROR:", e)
            time.sleep(10)
