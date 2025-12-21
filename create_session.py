from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from config import API_ID, API_HASH

def get_phone():
    return input("Telefon raqamingizni kiriting (+998XXYYYYYYY): ")

print("=" * 50)
print("TELEGRAM SESSION YARATISH")
print("=" * 50)
print(f"API_ID: {API_ID}")
print(f"API_HASH: {API_HASH}")
print("=" * 50)

try:
    client = TelegramClient("user_session", API_ID, API_HASH)
    print("1. Client yaratildi")
    
    # start() metodi avtomatik ravishda ulanish va autentifikatsiya qiladi
    client.start(phone=get_phone)
    print("2. Telegram serveriga ulandi va tizimga kirdingiz")
    
    print(">>> SESSION MUVAFFAQIYATLI YARATILDI! <<<")
    
    # client avtomatik ravishda yopiladi
    print("✅ TAYYOR! Session fayli yaratildi")

except FloodWaitError as e:
    print(f"❌ Telegram blokladi! {e.seconds} sekund kutish kerak")
except Exception as e:
    print(f"❌ Xatolik: {type(e).__name__}: {e}")