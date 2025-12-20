from telethon.sync import TelegramClient
from config import API_ID, API_HASH

print("Session yaratilmoqda...")
client = TelegramClient("session", API_ID, API_HASH)
client.start()
print("✅ Session yaratildi! Endi git push qiling.")
client.disconnect()
