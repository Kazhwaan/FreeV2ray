import os
import requests

# گرفتن اطلاعات حساس از تنظیمات امن گیت‌هاب
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# لینک مستقیم به فایل کانفیگ‌ها در مخزن هدف
SOURCE_URL = "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/V2Ray-Config-By-EbraSha-All-Type.txt"

def fetch_and_send():
    try:
        response = requests.get(SOURCE_URL)
        # جدا کردن خط به خط متن
        lines = response.text.strip().split('\n')

        # گرفتن ۱۰ خط آخر که خالی نیستند
        configs = [line for line in lines if line.strip()][-10:]

        if not configs:
            return

        message = "⚡️ آخرین آپدیت کانفیگ‌ها:\n\n" + "\n\n".join(configs)

        # ارسال به تلگرام
        api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_ID,
            "text": message,
            "disable_web_page_preview": True
        }
        requests.post(api_url, json=payload)
        print("Sent successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_send()
