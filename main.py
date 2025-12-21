# -*- coding: utf-8 -*-
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
    global clock_on, online_on
    await client.start()
    print("[OK] Telethon ulandi")
    while True:
        if clock_on:
            tashkent = pytz.timezone('Asia/Tashkent')
            now = datetime.now(tashkent)
            text = now.strftime('%H:%M')
            try:
                await client(UpdateProfileRequest(first_name=text))
                print(f"[CLOCK] Nickname: {text}")
            except Exception as e:
                print(f"[ERROR] {e}")
        
        if online_on:
            try:
                await client(UpdateStatusRequest(offline=False))
                print("[ONLINE] Active")
            except Exception as e:
                print(f"[ERROR] {e}")
        await asyncio.sleep(UPDATE_INTERVAL)

# ================= AUTO XABAR =================
async def auto_message(bot_app):
    while True:
        try:
            tashkent = pytz.timezone('Asia/Tashkent')
            now = datetime.now(tashkent)
            await bot_app.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"[BOT STATUS]\n\nVaqt: {now.strftime('%H:%M')}\nSoat: {'ON' if clock_on else 'OFF'}\nOnline: {'ON' if online_on else 'OFF'}"
            )
        except Exception as e:
            print(f"[ERROR] Auto xabar: {e}")
        await asyncio.sleep(AUTO_MESSAGE_INTERVAL)


# ================= BOT BUYRUQLARI =================
def get_keyboard():
    clock_status = "ON" if clock_on else "OFF"
    online_status = "ON" if online_on else "OFF"
    return [
        [InlineKeyboardButton(f"\u23f0 SOAT [{clock_status}]", callback_data="toggle_clock")],
        [InlineKeyboardButton(f"\U0001f7e2 ONLINE [{online_status}]", callback_data="toggle_online")],
        [InlineKeyboardButton("\U0001f4ca STATISTIKA", callback_data="stats")],
        [InlineKeyboardButton("\U0001f504 YANGILASH", callback_data="refresh")]
    ]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("Sizga ruxsat yo'q!")
        return
    
    tashkent = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tashkent)
    
    text = f"""
\U0001f3ae BOSHQARUV PANELI

\u23f0 Vaqt: {now.strftime('%H:%M:%S')}
\U0001f4c5 Sana: {now.strftime('%d.%m.%Y')}

\U0001f551 Soat: {'YOQILGAN \u2705' if clock_on else 'OCHIRILGAN \u274c'}
\U0001f7e2 Online: {'YOQILGAN \u2705' if online_on else 'OCHIRILGAN \u274c'}

\U0001f447 Tugmalardan foydalaning:
"""
    
    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(get_keyboard())
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global clock_on, online_on
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.answer("Ruxsat yo'q!", show_alert=True)
        return
    
    if not anti_flood(query.from_user.id):
        await query.answer("Sekinroq!", show_alert=True)
        return
    
    stats = load_stats()
    tashkent = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tashkent)
    
    if query.data == "toggle_clock":
        clock_on = not clock_on
        if clock_on:
            stats["clock_on_count"] += 1
            save_stats(stats)
        status = "YOQILDI \u2705" if clock_on else "OCHIRILDI \u274c"
        await query.message.edit_text(
            f"\u23f0 SOAT {status}\n\n\U0001f552 Vaqt: {now.strftime('%H:%M:%S')}",
            reply_markup=InlineKeyboardMarkup(get_keyboard())
        )
    
    elif query.data == "toggle_online":
        online_on = not online_on
        if not online_on:
            await client(UpdateStatusRequest(offline=True))
        status = "YOQILDI \u2705" if online_on else "OCHIRILDI \u274c"
        await query.message.edit_text(
            f"\U0001f7e2 ONLINE {status}\n\n\U0001f552 Vaqt: {now.strftime('%H:%M:%S')}",
            reply_markup=InlineKeyboardMarkup(get_keyboard())
        )
    
    elif query.data == "stats":
        await query.message.edit_text(
            f"\U0001f4ca STATISTIKA\n\n\u23f0 Soat yoqilgan: {stats['clock_on_count']} marta\n\U0001f552 Vaqt: {now.strftime('%H:%M:%S')}",
            reply_markup=InlineKeyboardMarkup(get_keyboard())
        )
    
    elif query.data == "refresh":
        text = f"""
\U0001f3ae BOSHQARUV PANELI

\u23f0 Vaqt: {now.strftime('%H:%M:%S')}
\U0001f4c5 Sana: {now.strftime('%d.%m.%Y')}

\U0001f551 Soat: {'YOQILGAN \u2705' if clock_on else 'OCHIRILGAN \u274c'}
\U0001f7e2 Online: {'YOQILGAN \u2705' if online_on else 'OCHIRILGAN \u274c'}
"""
        await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(get_keyboard())
        )


# ================= WEB ADMIN PANEL =================
@app_flask.route("/")
def web_home():
    tashkent = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tashkent)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Bot Panel</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial; background: #1a1a2e; color: #fff; text-align: center; padding: 50px; }}
            .status {{ font-size: 24px; margin: 20px; }}
            .on {{ color: #00ff00; }}
            .off {{ color: #ff0000; }}
            a {{ display: inline-block; margin: 10px; padding: 15px 30px; background: #4a4a6a; color: #fff; text-decoration: none; border-radius: 5px; }}
            a:hover {{ background: #6a6a8a; }}
        </style>
    </head>
    <body>
        <h1>TELEGRAM BOT PANEL</h1>
        <p>Vaqt: {now.strftime('%H:%M:%S')}</p>
        <div class="status">Soat: <span class="{'on' if clock_on else 'off'}">{'ON' if clock_on else 'OFF'}</span></div>
        <div class="status">Online: <span class="{'on' if online_on else 'off'}">{'ON' if online_on else 'OFF'}</span></div>
        <br>
        <a href="/clock/on">SOAT ON</a>
        <a href="/clock/off">SOAT OFF</a>
        <br>
        <a href="/online/on">ONLINE ON</a>
        <a href="/online/off">ONLINE OFF</a>
    </body>
    </html>
    """

@app_flask.route("/clock/on")
def clock_on_route():
    global clock_on
    clock_on = True
    return "<script>location.href='/'</script>"

@app_flask.route("/clock/off")
def clock_off_route():
    global clock_on
    clock_on = False
    return "<script>location.href='/'</script>"

@app_flask.route("/online/on")
def online_on_route():
    global online_on
    online_on = True
    return "<script>location.href='/'</script>"

@app_flask.route("/online/off")
def online_off_route():
    global online_on
    online_on = False
    return "<script>location.href='/'</script>"

def run_flask():
    app_flask.run(host="0.0.0.0", port=WEB_PORT)

# ================= ASOSIY =================
async def main():
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CallbackQueryHandler(buttons))
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("[OK] Web panel ishga tushdi")
    
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()
    print("[OK] Bot ishga tushdi")
    
    asyncio.create_task(clock_task())
    asyncio.create_task(auto_message(bot_app))
    print("[OK] Tasklar ishga tushdi")
    
    await asyncio.Event().wait()

if __name__ == "__main__":
    print("[START] Bot ishga tushmoqda...")
    asyncio.run(main())
