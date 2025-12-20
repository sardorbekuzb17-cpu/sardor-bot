from telethon.sync import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN

print("Bot session yaratilmoqda...")
client = TelegramClient("session", API_ID, API_HASH)
client.start(bot_token=BOT_TOKEN)
print("✅ Session yaratildi!")
client.disconnect()
