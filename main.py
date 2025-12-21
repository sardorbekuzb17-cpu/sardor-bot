import asyncio
import json
import time
import threading
from datetime import datetime
import pytz

# ===== TELETHON =====
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.account import UpdateStatusRequest

# ===== TELEGRAM BOT =====
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# ===== FLASK WEB PANEL =====
from flask import Flask

from config import *

# ================= GLOBAL HOLAT =================
clock_on = False
online_on = False
last_action = {}
client = TelegramClient("user_session", API_ID, API_HASH)
app_flask = Flask(__name__)

# ================= STATISTIKA =================
def load_stats():
    try:
        with open("stats.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"clock_on_count": 0}

def save_stats(data):
    with open("stats.json", "w") as f:
        json.dump(data, f)

# ================= ANTI-FLOOD =================
def anti_flood(user_id, delay=3):
    now = time.time()
    if user_id in last_action and now - last_action[user_id] < delay:
        return False
    last_action[user_id] = now
    return True

def is_admin(user_id):
    return user_id == ADMIN_ID


# ================= PROFIL SOATI =================
async def clock_task():
    global clock_on
    await client.start()
    print("✅ Telethon ulandi")
    while True:
        if clock_on:
            # Toshkent vaqti
            tashkent = pytz.timezone('Asia/Tashkent')
            now = datetime.now(tashkent)
            text = f"⏰ {now.strftime('%H:%M')}"
            try:
                await client(UpdateProfileRequest(first_name=text))
                print(f"Nickname yangilandi: {text}")
            except Exception as e:
                print(f"Xatolik: {e}")
        
        if online_on:
            try:
                await client(UpdateStatusRequest(offline=False))
                print("Online ✅")
            except Exception as e:
                print(f"Online xatolik: {e}")
        await asyncio.sleep(UPDATE_INTERVAL)

# ================= AUTO XABAR =================
async def auto_message(bot_app):
    while True:
        try:
            await bot_app.bot.send_message(
                chat_id=ADMIN_ID,
                text="🤖 Bot 24/7 ishlayapti, hammasi joyida ✅"
            )
        except Exception as e:
            print(f"Auto xabar xatosi: {e}")
        await asyncio.sleep(AUTO_MESSAGE_INTERVAL)

# ================= BOT BUYRUQLARI =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    
    keyboard = [
        [InlineKeyboardButton("⏰ Soatni YOQISH", callback_data="on")],
        [InlineKeyboardButton("⛔ Soatni O'CHIRISH", callback_data="off")],
        [InlineKeyboardButton("� Onlinet YOQISH", callback_data="online_on")],
        [InlineKeyboardButton("⚫ Online O'CHIRISH", callback_data="online_off")],
        [InlineKeyboardButton("📊 Statistika", callback_data="stats")]
    ]
    await update.message.reply_text(
        "🎛 Boshqaruv paneli",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global clock_on
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        return
    
    if not anti_flood(query.from_user.id):
        await query.answer("⏳ Sekinroq!", show_alert=True)
        return
    
    stats = load_stats()
    
    if query.data == "on":
        clock_on = True
        stats["clock_on_count"] += 1
        save_stats(stats)
        await query.message.reply_text("✅ Soat YOQILDI")
    
    elif query.data == "off":
        clock_on = False
        await query.message.reply_text("⛔ Soat O'CHDI")
    
    elif query.data == "stats":
        await query.message.reply_text(
            f"📊 Statistika:\n\n"
            f"⏰ Soat yoqilgan: {stats['clock_on_count']} marta"
        )
    
    elif query.data == "online_on":
        global online_on
        online_on = True
        await query.message.reply_text("🟢 Online YOQILDI - doim online ko'rinasiz")
    
    elif query.data == "online_off":
        online_on = False
        await client(UpdateStatusRequest(offline=True))
        await query.message.reply_text("⚫ Online O'CHIRILDI")


# ================= WEB ADMIN PANEL =================
@app_flask.route("/")
def web_home():
    return f"""
    <h2>Telegram Clock Panel</h2>
    <p>Holat: {"YOQILGAN" if clock_on else "O'CHIQ"}</p>
    <a href="/on">YOQISH</a> | 
    <a href="/off">O'CHIRISH</a>
    """

@app_flask.route("/on")
def web_on():
    global clock_on
    clock_on = True
    return "✅ Soat yoqildi"

@app_flask.route("/off")
def web_off():
    global clock_on
    clock_on = False
    return "⛔ Soat o'chirildi"

def run_flask():
    app_flask.run(host="0.0.0.0", port=WEB_PORT)

# ================= ASOSIY =================
async def main():
    # Bot yaratish
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CallbackQueryHandler(buttons))
    
    # Flask web panelni alohida threadda ishga tushirish
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Web panel ishga tushdi")
    
    # Botni ishga tushirish
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()
    print("🤖 Bot ishga tushdi")
    
    # Soat va auto xabar tasklarini ishga tushirish
    asyncio.create_task(clock_task())
    asyncio.create_task(auto_message(bot_app))
    print("⏰ Soat taski ishga tushdi")
    
    # Botni to'xtatmaslik uchun
    await asyncio.Event().wait()

if __name__ == "__main__":
    print("🚀 Bot ishga tushmoqda...")
    asyncio.run(main())
