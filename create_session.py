# -*- coding: utf-8 -*-
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from config import API_ID, API_HASH

print("Session yaratilmoqda...")

client = TelegramClient("user_session", API_ID, API_HASH)
client.connect()

phone = "+998200009121"

if not client.is_user_authorized():
    result = client.send_code_request(phone)
    print(f"Kod yuborildi!")
    print(f"Kod turi: {result.type}")
    print("")
    print("MUHIM: Kod Telegram ilovasiga yoki emailga kelishi mumkin!")
    print("Telegram ilovasini va emailingizni tekshiring.")
    print("")
    
    try:
        code = input("Kodni kiriting: ")
        client.sign_in(phone, code)
    except SessionPasswordNeededError:
        print("2FA parol kerak!")
        password = input("2FA parolni kiriting: ")
        client.sign_in(password=password)

me = client.get_me()
print(f"✅ Tayyor! Akkaunt: {me.first_name} (ID: {me.id})")
client.disconnect()
print("Session fayli yaratildi: user_session.session")
