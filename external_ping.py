#!/usr/bin/env python3
"""
Tashqi ping script - boshqa serverda ishlatish uchun
Bu script har 5 minutda botga ping yuboradi
"""

import requests
import time
from datetime import datetime

BOT_URL = "http://sardorsoatbot.alwaysdata.net"
PING_INTERVAL = 300  # 5 minut

def ping_bot():
    """Botga ping yuborish"""
    try:
        response = requests.get(f"{BOT_URL}/ping", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Bot ishlayapti - {data.get('time', 'N/A')}")
            return True
        else:
            print(f"⚠️ [{datetime.now().strftime('%H:%M:%S')}] Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Xatolik: {e}")
        return False

def main():
    """Asosiy loop"""
    print("🚀 Tashqi ping boshlandi")
    print(f"📍 URL: {BOT_URL}")
    print(f"⏱️ Interval: {PING_INTERVAL} sekund")
    print("-" * 50)
    
    while True:
        ping_bot()
        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    main()
