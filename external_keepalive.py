#!/usr/bin/env python3
"""
Tashqi serverdan ishlaydigan keepalive script
Bu scriptni boshqa serverda (masalan, PythonAnywhere, Replit) ishga tushiring
"""
import requests
import time
from datetime import datetime

# Alwaysdata bot URL'i
BOT_URL = "http://185.31.41.85:8080"
RESTART_URL = "http://185.31.41.85:8080/restart"

def check_bot():
    """Botni tekshirish"""
    try:
        response = requests.get(BOT_URL, timeout=10)
        if response.status_code == 200:
            print(f"{datetime.now()}: Bot ishlayapti ✓")
            return True
        else:
            print(f"{datetime.now()}: Bot javob bermadi (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"{datetime.now()}: Bot ulanmadi: {e}")
        return False

def restart_bot():
    """Botni qayta ishga tushirish"""
    try:
        response = requests.get(RESTART_URL, timeout=10)
        print(f"{datetime.now()}: Restart signal yuborildi")
        return True
    except Exception as e:
        print(f"{datetime.now()}: Restart xatosi: {e}")
        return False

if __name__ == "__main__":
    print("External keepalive started...")
    fail_count = 0
    
    while True:
        if check_bot():
            fail_count = 0
        else:
            fail_count += 1
            print(f"Fail count: {fail_count}")
            
            if fail_count >= 3:
                print("Bot 3 marta javob bermadi, restart...")
                restart_bot()
                fail_count = 0
                time.sleep(30)  # 30 sekund kutish
        
        time.sleep(300)  # 5 minut
