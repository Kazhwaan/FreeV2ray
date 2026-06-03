import os
import time
import requests
import urllib.parse
import re

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# لینک مستقیم فقط به فایل کانفیگ‌های Vless
SOURCE_URL = "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/vless_configs.txt"

def parse_config(config_link):
    """استخراج آدرس و نام از داخل لینک Vless"""
    address = "نامشخص"
    name = "نامشخص"
    try:
        if config_link.startswith("vless://"):
            match_host = re.search(r'@([^:]+):', config_link)
            if match_host:
                address = match_host.group(1)
            if "#" in config_link:
                name = urllib.parse.unquote(config_link.split("#")[1])
    except Exception:
        pass
        
    return address, name

def fetch_and_send():
    try:
        response = requests.get(SOURCE_URL)
        lines = response.text.strip().split('\n')
        
        # فیلتر کردن کانفیگ‌ها و انتخاب ۱۰ تای آخر که حتما با vless شروع بشن
        configs = [line for line in lines if line.strip() and line.startswith("vless://")][-10:]

        if not configs:
            print("No configs found!")
            return

        for i, config in enumerate(configs, start=1):
            address, name = parse_config(config)
            
            message = f"<b>🚀 سرور {i}</b>\n"
            message += f"<b>📍 لوکیشن:</b> {name}\n"
            message += f"<b>🌐 آدرس:</b> <code>{address}</code>\n\n"
            message += f"<b>👇 اتصال:</b>\n"
            message += f"<code>{config}</code>"

            api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": CHANNEL_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            }
            requests.post(api_url, json=payload)
            # یک ثانیه وقفه بین هر پیام برای جلوگیری از بلاک شدن توسط تلگرام
            time.sleep(1) 
            
        print("Vless configs sent successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_send()
