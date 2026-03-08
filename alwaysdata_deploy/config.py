import os
from dotenv import load_dotenv

load_dotenv()

# ===== TELEGRAM API =====
API_ID = int(os.getenv("API_ID", "34242979"))
API_HASH = os.getenv("API_HASH", "fbdacdc6070f84920b8a5d5a9011625e")

# ===== TELEGRAM BOT =====
BOT_TOKEN = os.getenv("BOT_TOKEN", "8027836128:AAHYnHIoujdmR9RcRQJ2bZMDBkUQjdXxvmE")

# ===== ADMIN =====
ADMIN_ID = int(os.getenv("ADMIN_ID", "6466528403"))

# ===== SOZLAMALAR =====
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "120"))
AUTO_MESSAGE_INTERVAL = int(os.getenv("AUTO_MESSAGE_INTERVAL", "21600"))
WEB_PORT = int(os.getenv("WEB_PORT", "8080"))
TIME_OFFSET_SECONDS = 0  # Toshkent vaqti bilan aynan bir xil
