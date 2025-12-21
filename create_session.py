from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from config import API_ID, API_HASH

print("Session yaratilmoqda...")

client = TelegramClient("user_session", API_ID, API_HASH)
client.connect()

phone = "+998200009121"

if not client.is_user_authorized():
    client.send_code_request(phone)
    print("Kod yuborildi! Telegram ilovasini tekshiring.")
    
    try:
        code = input("Kodni kiriting: ")
        client.sign_in(phone, code)
    except SessionPasswordNeededError:
        password = input("2FA parolni kiriting: ")
        client.sign_in(password=password)

me = client.get_me()
print(f"✅ Tayyor! Akkaunt: {me.first_name}")
client.disconnect()
