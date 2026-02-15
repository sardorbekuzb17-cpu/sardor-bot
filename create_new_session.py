from telethon import TelegramClient
from config import API_ID, API_HASH

client = TelegramClient("user_session", API_ID, API_HASH)

async def main():
    await client.start()
    print("Session yaratildi!")
    me = await client.get_me()
    print(f"Login: {me.first_name}")
    await client.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
