# -*- coding: utf-8 -*-
import asyncio
import json
import time
import threading
from datetime import datetime
import pytz

from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.account import UpdateStatusRequest

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from flask import Flask
from config import *

clock_on = True
online_on = True
last_action = {}
client = TelegramClient("user_session", API_ID, API_HASH)
app_flask = Flask(__name__)

def load_stats():
    try:
        with open("stats.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"clock_on_count": 0}

def save_stats(data):
    with open("stats.json", "w") as f:
        json.dump(data, f)

def anti_flood(user_id, delay=3):
    now = time.time()
    if user_id in last_action and now - last_action[user_id] < delay:
        return False
    last_action[user_id] = now
    return True

def is_admin(user_id):
    return user_id == ADMIN_ID

async def clock_task():
    global clock_on, online_on
    await client.start()
    print("Telethon ulandi")
    while True:
        if clock_on:
            tashkent = pytz.timezone('Asia/Tashkent')
            now = datetime.now(tashkent)
            # Qalin raqamlar (Unicode bold)
            bold_nums = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵', ':': ':'}
            time_str = now.strftime('%H:%M')
            text = ''.join(bold_nums.get(c, c) for c in time_str)
            try:
                await client(UpdateProfileRequest(first_name=text))
                print(f"Nickname: {text}")
            except Exception as e:
                print(f"Xatolik: {e}")
        
        if online_on:
            try:
                await client(UpdateStatusRequest(offline=False))
            except Exception as e:
                print(f"Online xatolik: {e}")
        await asyncio.sleep(UPDATE_INTERVAL)

async def auto_message(bot_app):
    while True:
        try:
            tashkent = pytz.timezone('Asia/Tashkent')
            now = datetime.now(tashkent)
            clock_emoji = chr(0x23F0)
            green_emoji = chr(0x1F7E2)
            check = chr(0x2705)
            cross = chr(0x274C)
            clock_status = f"ON {check}" if clock_on else f"OFF {cross}"
            online_status = f"ON {check}" if online_on else f"OFF {cross}"
            msg = f"BOT STATUS\n\nVaqt: {now.strftime('%H:%M')}\n{clock_emoji} Soat: {clock_status}\n{green_emoji} Online: {online_status}"
            await bot_app.bot.send_message(chat_id=ADMIN_ID, text=msg)
        except Exception as e:
            print(f"Auto xabar xatosi: {e}")
        await asyncio.sleep(AUTO_MESSAGE_INTERVAL)


def get_keyboard():
    clock_emoji = chr(0x23F0)
    green_emoji = chr(0x1F7E2)
    stats_emoji = chr(0x1F4CA)
    refresh_emoji = chr(0x1F504)
    clock_status = "ON" if clock_on else "OFF"
    online_status = "ON" if online_on else "OFF"
    return [
        [InlineKeyboardButton(f"{clock_emoji} SOAT [{clock_status}]", callback_data="toggle_clock")],
        [InlineKeyboardButton(f"{green_emoji} ONLINE [{online_status}]", callback_data="toggle_online")],
        [InlineKeyboardButton(f"{stats_emoji} STATISTIKA", callback_data="stats")],
        [InlineKeyboardButton(f"{refresh_emoji} YANGILASH", callback_data="refresh")]
    ]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("Sizga ruxsat yoq!")
        return
    
    tashkent = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tashkent)
    
    panel_emoji = chr(0x1F3AE)
    clock_emoji = chr(0x23F0)
    calendar_emoji = chr(0x1F4C5)
    green_emoji = chr(0x1F7E2)
    check = chr(0x2705)
    cross = chr(0x274C)
    down_emoji = chr(0x1F447)
    
    clock_status = f"YOQILGAN {check}" if clock_on else f"OCHIRILGAN {cross}"
    online_status = f"YOQILGAN {check}" if online_on else f"OCHIRILGAN {cross}"
    
    text = f"""{panel_emoji} BOSHQARUV PANELI

{clock_emoji} Vaqt: {now.strftime('%H:%M:%S')}
{calendar_emoji} Sana: {now.strftime('%d.%m.%Y')}

{clock_emoji} Soat: {clock_status}
{green_emoji} Online: {online_status}

{down_emoji} Tugmalardan foydalaning:"""
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(get_keyboard()))

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global clock_on, online_on
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.answer("Ruxsat yoq!", show_alert=True)
        return
    
    if not anti_flood(query.from_user.id):
        await query.answer("Sekinroq!", show_alert=True)
        return
    
    stats = load_stats()
    tashkent = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tashkent)
    
    clock_emoji = chr(0x23F0)
    green_emoji = chr(0x1F7E2)
    stats_emoji = chr(0x1F4CA)
    check = chr(0x2705)
    cross = chr(0x274C)
    
    if query.data == "toggle_clock":
        clock_on = not clock_on
        if clock_on:
            stats["clock_on_count"] += 1
            save_stats(stats)
        status = f"YOQILDI {check}" if clock_on else f"OCHIRILDI {cross}"
        await query.message.edit_text(f"{clock_emoji} SOAT {status}\n\nVaqt: {now.strftime('%H:%M:%S')}", reply_markup=InlineKeyboardMarkup(get_keyboard()))
    
    elif query.data == "toggle_online":
        online_on = not online_on
        if not online_on:
            await client(UpdateStatusRequest(offline=True))
        status = f"YOQILDI {check}" if online_on else f"OCHIRILDI {cross}"
        await query.message.edit_text(f"{green_emoji} ONLINE {status}\n\nVaqt: {now.strftime('%H:%M:%S')}", reply_markup=InlineKeyboardMarkup(get_keyboard()))
    
    elif query.data == "stats":
        await query.message.edit_text(f"{stats_emoji} STATISTIKA\n\nSoat yoqilgan: {stats['clock_on_count']} marta\nVaqt: {now.strftime('%H:%M:%S')}", reply_markup=InlineKeyboardMarkup(get_keyboard()))
    
    elif query.data == "refresh":
        panel_emoji = chr(0x1F3AE)
        calendar_emoji = chr(0x1F4C5)
        down_emoji = chr(0x1F447)
        clock_status = f"YOQILGAN {check}" if clock_on else f"OCHIRILGAN {cross}"
        online_status = f"YOQILGAN {check}" if online_on else f"OCHIRILGAN {cross}"
        text = f"""{panel_emoji} BOSHQARUV PANELI

{clock_emoji} Vaqt: {now.strftime('%H:%M:%S')}
{calendar_emoji} Sana: {now.strftime('%d.%m.%Y')}

{clock_emoji} Soat: {clock_status}
{green_emoji} Online: {online_status}"""
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(get_keyboard()))


@app_flask.route("/")
def web_home():
    tashkent = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tashkent)
    clock_class = "on" if clock_on else "off"
    online_class = "on" if online_on else "off"
    return f"""<!DOCTYPE html>
<html><head><title>Bot Panel</title><meta charset="utf-8">
<style>body{{font-family:Arial;background:#1a1a2e;color:#fff;text-align:center;padding:50px}}
.on{{color:#0f0}}.off{{color:#f00}}a{{display:inline-block;margin:10px;padding:15px 30px;background:#4a4a6a;color:#fff;text-decoration:none;border-radius:5px}}</style></head>
<body><h1>BOT PANEL</h1><p>Vaqt: {now.strftime('%H:%M:%S')}</p>
<p>Soat: <span class="{clock_class}">{"ON" if clock_on else "OFF"}</span></p>
<p>Online: <span class="{online_class}">{"ON" if online_on else "OFF"}</span></p>
<a href="/clock/on">SOAT ON</a><a href="/clock/off">SOAT OFF</a><br>
<a href="/online/on">ONLINE ON</a><a href="/online/off">ONLINE OFF</a></body></html>"""

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

async def main():
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CallbackQueryHandler(buttons))
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()
    
    asyncio.create_task(clock_task())
    asyncio.create_task(auto_message(bot_app))
    
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
