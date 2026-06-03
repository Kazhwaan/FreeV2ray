import os
import time
import requests
import urllib.parse
import base64
import json
import re

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
SOURCE_URL = "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/V2Ray-Config-By-EbraSha-All-Type.txt"

def parse_config(config_link):
    """تابع برای استخراج آدرس و نام از داخل لینک کانفیگ"""
    address = "نامشخص"
    name = "نامشخص"
    try:
        # برای vless و trojan
        if config_link.startswith("vless://") or config_link.startswith("trojan://"):
            match_host = re.search(r'@([^:]+):', config_link)
            if match_host:
                address = match_host.group(1)
            if "#" in config_link:
                name = urllib.parse.unquote(config_link.split("#")[1])
                
        # برای vmess (چون کدگذاری شده است باید دیکد شود)
        elif config_link.startswith("vmess://"):
            b64_str = config_link.replace("vmess://", "")
            # اضافه کردن = برای جلوگیری از ارور پدینگ बेस64
            b64_str += "=" * ((4 - len(b64_str) % 4) % 4)
            decoded = base64.b64decode(b64_str).decode('utf-8')
            data = json.loads(decoded)
            address = data.get("add", "نامشخص")
            name = data.get("ps", "نامشخص")
            
        # برای shadowsocks
        elif config_link.startswith("ss://"):
            if "#" in config_link:
                name = urllib.parse.unquote(config_link.split("#")[1])
    except Exception:
        pass # اگر خطایی در خوندن لینک بود از روش رد شو
        
    return address, name

def fetch_and_send():
    try:
        response = requests.get(SOURCE_URL)
        lines = response.text.strip().split('\n')
        # گرفتن ۱۰ کانفیگ آخر
        configs = [line for line in lines if line.strip()][-10:]

        if not configs:
            return

        # ارسال کانفیگ‌ها یکی یکی برای قشنگ‌تر شدن ظاهر (مثل عکس)
        for i, config in enumerate(configs, start=1):
            address, name = parse_config(config)
            
            # ساختار پیام با تگ‌های HTML برای بولد کردن و کپی راحت
            message = f"<b>🚀 سرور {i}</b>\n"
            message += f"<b>📍 لوکیشن:</b> {name}\n"
            message += f"<b>🌐 آدرس:</b> <code>{address}</code>\n\n"
            message += f"<b>👇 اتصال:</b>\n"
            message += f"<code>{config}</code>" # تگ code باعث میشه با یه کلیک کپی بشه

            api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": CHANNEL_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            }
            requests.post(api_url, json=payload)
            # یک ثانیه وقفه بین هر پیام که تلگرام ربات رو اسپم تشخیص نده
            time.sleep(1) 
            
        print("All messages sent beautifully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_send()
