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
time_offset = 0  # Toshkent vaqti bilan aynan bir xil
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

async def keepalive_task():
    """Telethon connectionni doimiy saqlash va avtomatik reconnect"""
    reconnect_count = 0
    while True:
        try:
            if client.is_connected():
                # Har 2 minutda ping yubor
                await client.get_me()
                print(f"Keepalive: Connection active (reconnects: {reconnect_count})")
                reconnect_count = 0  # Reset counter
            else:
                print("Keepalive: Disconnected! Reconnecting...")
                reconnect_count += 1
                await client.disconnect()
                await asyncio.sleep(2)
                await client.connect()
                if await client.is_user_authorized():
                    print(f"Keepalive: Reconnected successfully (attempt {reconnect_count})")
                else:
                    print("Keepalive: Session expired! Bot needs restart.")
        except ConnectionError as e:
            print(f"Keepalive connection error: {e}, reconnecting...")
            reconnect_count += 1
            try:
                await client.disconnect()
                await asyncio.sleep(5)
                await client.connect()
            except:
                pass
        except Exception as e:
            print(f"Keepalive xatolik: {e}")
            reconnect_count += 1
        
        await asyncio.sleep(120)  # 2 minut

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
            try:
                await bot_app.bot.send_message(chat_id=ADMIN_ID, text=msg)
            except Exception as e:
                print(f"Auto xabar xatosi: {e}")
        except Exception as e:
            print(f"Auto message loop xatolik: {e}")
        await asyncio.sleep(AUTO_MESSAGE_INTERVAL)


def get_keyboard():
    clock_emoji = chr(0x23F0)
    green_emoji = chr(0x1F7E2)
    stats_emoji = chr(0x1F4CA)
    refresh_emoji = chr(0x1F504)
    plus_emoji = chr(0x2795)
    minus_emoji = chr(0x2796)
    restart_emoji = chr(0x1F504)
    clock_status = "ON" if clock_on else "OFF"
    online_status = "ON" if online_on else "OFF"
    return [
        [InlineKeyboardButton(f"{clock_emoji} SOAT [{clock_status}]", callback_data="toggle_clock")],
        [InlineKeyboardButton(f"{green_emoji} ONLINE [{online_status}]", callback_data="toggle_online")],
        [
            InlineKeyboardButton(f"{minus_emoji} 5s", callback_data="offset_minus"),
            InlineKeyboardButton(f"{clock_emoji} {time_offset}s", callback_data="show_offset"),
            InlineKeyboardButton(f"{plus_emoji} 5s", callback_data="offset_plus")
        ],
        [InlineKeyboardButton(f"{stats_emoji} STATISTIKA", callback_data="stats")],
        [InlineKeyboardButton(f"{restart_emoji} BOTNI QAYTA ISHGA TUSHIRISH", callback_data="restart_bot")],
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
    global clock_on, online_on, time_offset
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
    
    elif query.data == "offset_plus":
        time_offset += 5
        # Darhol nickname yangilash
        from datetime import timedelta
        tashkent_tz = pytz.timezone('Asia/Tashkent')
        new_time = datetime.now(tashkent_tz) + timedelta(seconds=time_offset)
        bold_nums = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵', ':': ':'}
        time_str = new_time.strftime('%H:%M')
        text_name = ''.join(bold_nums.get(c, c) for c in time_str)
        try:
            await client(UpdateProfileRequest(first_name=text_name))
        except:
            pass
        await query.message.edit_text(f"{clock_emoji} Vaqt sozlamasi: {time_offset} sekund\n\nVaqt: {now.strftime('%H:%M:%S')}", reply_markup=InlineKeyboardMarkup(get_keyboard()))
    
    elif query.data == "offset_minus":
        time_offset -= 5
        # Darhol nickname yangilash
        from datetime import timedelta
        tashkent_tz = pytz.timezone('Asia/Tashkent')
        new_time = datetime.now(tashkent_tz) + timedelta(seconds=time_offset)
        bold_nums = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵', ':': ':'}
        time_str = new_time.strftime('%H:%M')
        text_name = ''.join(bold_nums.get(c, c) for c in time_str)
        try:
            await client(UpdateProfileRequest(first_name=text_name))
        except:
            pass
        await query.message.edit_text(f"{clock_emoji} Vaqt sozlamasi: {time_offset} sekund\n\nVaqt: {now.strftime('%H:%M:%S')}", reply_markup=InlineKeyboardMarkup(get_keyboard()))
    
    elif query.data == "show_offset":
        await query.answer(f"Hozirgi offset: {time_offset} sekund", show_alert=True)
    
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
    
    elif query.data == "restart_bot":
        restart_emoji = chr(0x1F504)
        await query.message.edit_text(f"{restart_emoji} Bot qayta ishga tushirilmoqda...\n\nIltimos kuting...", reply_markup=None)
        
        # Botni qayta ishga tushirish
        import os
        import sys
        try:
            # Restart script
            os.execv(sys.executable, ['python3'] + sys.argv)
        except Exception as e:
            await query.message.edit_text(f"❌ Xatolik: {e}\n\n🔧 Qo'lda qayta ishga tushiring:\nSSH: bash start_bot.sh", reply_markup=InlineKeyboardMarkup(get_keyboard()))


@app_flask.route("/")
def web_home():
    tashkent = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tashkent)
    clock_class = "on" if clock_on else "off"
    online_class = "on" if online_on else "off"
    return f"""<!DOCTYPE html>
<html lang="uz"><head><title>Sardor Bot Keepalive</title><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>body{{font-family:Arial;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}}
.container{{text-align:center;background:rgba(255,255,255,0.1);padding:40px;border-radius:20px;backdrop-filter:blur(10px);max-width:600px}}
h1{{margin:0 0 20px 0}}#status{{font-size:24px;margin:20px 0}}.success{{color:#4ade80}}.on{{color:#4ade80}}.off{{color:#f87171}}
a{{display:inline-block;margin:10px;padding:15px 30px;background:rgba(255,255,255,0.2);color:#fff;text-decoration:none;border-radius:10px;transition:0.3s}}
a:hover{{background:rgba(255,255,255,0.3)}}</style>
<script>
async function pingBot(){{try{{const r=await fetch('/ping');const d=await r.json();document.getElementById('status').className='success';document.getElementById('status').innerHTML='✅ Bot ishlayapti!';document.getElementById('info').innerHTML=`<p>Vaqt: ${{d.time}}</p><p>Sana: ${{d.date}}</p><p>Soat: ${{d.clock}}</p><p>Online: ${{d.online}}</p>`}}catch(e){{document.getElementById('status').className='error';document.getElementById('status').innerHTML='❌ Bot javob bermadi'}}}}
pingBot();setInterval(pingBot,300000);
</script></head>
<body><div class="container"><h1>🤖 Sardor Bot Keepalive</h1>
<div id="status" class="success">✅ Bot ishlayapti!</div>
<div id="info"><p>Vaqt: {now.strftime('%H:%M:%S')}</p><p>Sana: {now.strftime('%d.%m.%Y')}</p>
<p>Soat: <span class="{clock_class}">{"ON" if clock_on else "OFF"}</span></p>
<p>Online: <span class="{online_class}">{"ON" if online_on else "OFF"}</span></p></div>
<div style="margin-top:30px"><a href="/clock/on">SOAT ON</a><a href="/clock/off">SOAT OFF</a><br>
<a href="/online/on">ONLINE ON</a><a href="/online/off">ONLINE OFF</a></div></div></body></html>"""

@app_flask.route("/health")
def health():
    """Keepalive endpoint - Fly.io uchun"""
    return {"status": "ok", "time": datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%H:%M:%S')}

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

@app_flask.route("/restart")
def restart_route():
    """Tashqi keepalive uchun restart endpoint"""
    import os
    import sys
    import threading
    
    def do_restart():
        time.sleep(1)
        os.execv(sys.executable, ['python3.11'] + sys.argv)
    
    threading.Thread(target=do_restart, daemon=True).start()
    return {"status": "restarting", "message": "Bot qayta ishga tushmoqda..."}

@app_flask.route("/ping")
def ping_route():
    """UptimeRobot/cron-job.org uchun keepalive endpoint"""
    tashkent = pytz.timezone('Asia/Tashkent')
    now = datetime.now(tashkent)
    
    # Bot statusini tekshirish
    bot_status = "running" if clock_on or online_on else "idle"
    
    return {
        "status": "ok",
        "bot": "Sardor Clock Bot",
        "time": now.strftime('%H:%M:%S'),
        "date": now.strftime('%d.%m.%Y'),
        "clock": "ON" if clock_on else "OFF",
        "online": "ON" if online_on else "OFF",
        "bot_status": bot_status,
        "uptime": "running"
    }

def run_flask():
    import os
    port = int(os.environ.get("PORT", WEB_PORT))
    # Production uchun threaded=True
    app_flask.run(host="0.0.0.0", port=port, threaded=True, use_reloader=False)

async def auto_restart_task():
    """Har 12 soatda botni avtomatik qayta ishga tushirish"""
    while True:
        await asyncio.sleep(43200)  # 12 soat
        print("Auto-restart: 12 soat o'tdi, bot qayta ishga tushmoqda...")
        import os
        import sys
        os.execv(sys.executable, ['python3.11'] + sys.argv)

async def self_ping_task():
    """O'zini o'zi ping qilish - bot uyg'oq turadi"""
    import aiohttp
    while True:
        await asyncio.sleep(300)  # 5 minut
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:8080/ping', timeout=10) as resp:
                    if resp.status == 200:
                        print("Self-ping: OK")
                    else:
                        print(f"Self-ping: Status {resp.status}")
        except Exception as e:
            print(f"Self-ping xatolik: {e}")

async def main():
    import os
    import base64
    
    # SESSION_BASE64 dan session yaratish
    session_b64 = os.environ.get("SESSION_BASE64")
    if session_b64 and not os.path.exists("user_session.session"):
        try:
            session_bytes = base64.b64decode(session_b64)
            with open("user_session.session", "wb") as f:
                f.write(session_bytes)
            print("Session base64 dan yaratildi")
        except Exception as e:
            print(f"Session decode xatosi: {e}")
    
    # Session fayli borligini tekshirish
    if not os.path.exists("user_session.session"):
        print("XATOLIK: user_session.session fayli topilmadi!")
        print("Iltimos, session faylini yuklang yoki SESSION_BASE64 o'zgaruvchisini qo'shing.")
        return
    
    # Avval Telethon ulansin
    try:
        await client.connect()
        if not await client.is_user_authorized():
            print("XATOLIK: Session yaroqsiz!")
            print("create_session.py ni ishga tushiring va yangi session yarating.")
            return
        me = await client.get_me()
        print(f"Telethon ulandi: {me.first_name} (ID: {me.id})")
    except Exception as e:
        print(f"Telethon ulanish xatosi: {e}")
        return
    
    # Flask thread
    flask_thread = threading.Thread(target=run_flask, daemon=False)  # daemon=False - to'xtamaydi
    flask_thread.start()
    
    # Telegram Bot ishga tushirish
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CallbackQueryHandler(buttons))
    
    # Background tasks
    asyncio.create_task(clock_loop())
    asyncio.create_task(keepalive_task())
    asyncio.create_task(auto_message(bot_app))
    asyncio.create_task(auto_restart_task())
    asyncio.create_task(self_ping_task())
    
    print("Bot to'liq ishga tushdi")
    
    # Bot'ni ishga tushirish
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()
    
    await asyncio.Event().wait()

async def clock_loop():
    global clock_on, online_on
    flood_wait_until = 0  # Flood limit tugash vaqti
    last_update_time = ""  # Oxirgi yangilangan vaqt
    error_count = 0  # Xatoliklar soni
    
    # SARDOR animatsiyasi uchun
    text_animation = "SARDOR "
    animation_index = 0
    
    while True:
        # Reconnect agar ulanish uzilgan bo'lsa
        if not client.is_connected():
            try:
                await client.connect()
                print("Reconnected to Telegram")
            except Exception as e:
                print(f"Reconnect xatolik: {e}")
                await asyncio.sleep(5)
                continue
        try:
            # Flood limit tekshirish
            import time as time_module
            if flood_wait_until > 0 and time_module.time() < flood_wait_until:
                wait_time = int(flood_wait_until - time_module.time())
                if wait_time > 0:
                    print(f"Flood limit: {wait_time} sekund kutish kerak")
                    await asyncio.sleep(min(wait_time, 60))
                    continue
            
            if clock_on:
                tashkent = pytz.timezone('Asia/Tashkent')
                from datetime import timedelta
                now = datetime.now(tashkent) + timedelta(seconds=time_offset)
                bold_nums = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵', ':': ':'}
                time_str = now.strftime('%H:%M')
                time_text = ''.join(bold_nums.get(c, c) for c in time_str)
                
                # SARDOR animatsiyasi - har daqiqada bir harf (qalin yozuvda)
                animated_part = text_animation[:animation_index + 1]
                # SARDOR ni ham qalin yozuvda
                bold_letters = {
                    'S': '𝗦', 'A': '𝗔', 'R': '𝗥', 'D': '𝗗', 'O': '𝗢', ' ': ' '
                }
                animated_text = ''.join(bold_letters.get(c, c) for c in animated_part)
                full_text = f"{time_text} {animated_text}"
                
                # Faqat vaqt yoki animatsiya o'zgarganda yangilash
                if full_text != last_update_time:
                    try:
                        if client.is_connected():
                            await client(UpdateProfileRequest(first_name=full_text))
                            print(f"Nickname yangilandi: {full_text}")
                            last_update_time = full_text
                            flood_wait_until = 0  # Reset flood limit
                            error_count = 0  # Reset error count
                        else:
                            print("Telethon ulanmagan, qayta ulanmoqda...")
                            await client.connect()
                    except Exception as e:
                        error_msg = str(e)
                        error_count += 1
                        
                        if "wait" in error_msg.lower() and "seconds" in error_msg.lower():
                            # Flood limit - kutish vaqtini saqlash
                            import re
                            wait_time = re.search(r'(\d+) seconds', error_msg)
                            if wait_time:
                                wait_seconds = int(wait_time.group(1))
                                flood_wait_until = time_module.time() + wait_seconds
                                print(f"Flood limit: {wait_seconds} sekund kutish kerak")
                                await asyncio.sleep(min(wait_seconds, 60))
                                continue
                        elif "authorization key" in error_msg.lower():
                            error_text = f"⚠️ XATOLIK: Session yaroqsiz!\n\nSabab: {error_msg}\n\n🔧 Bartaraf qilish:\n1. SSH orqali ulaning\n2. Buyruq: cd ~ && rm -f user_session.session\n3. Buyruq: python3 create_session.py\n4. Telefon raqamingizga kelgan kodni kiriting\n5. Buyruq: bash start_bot.sh\n\nBot to'xtadi."
                            print(error_text)
                            try:
                                # Telegram botga xabar yuborish
                                bot_app_temp = ApplicationBuilder().token(BOT_TOKEN).build()
                                await bot_app_temp.bot.send_message(chat_id=ADMIN_ID, text=error_text)
                            except:
                                pass
                            return  # Bot to'xtaydi
                        else:
                            print(f"Xatolik #{error_count}: {e}")
                            
                            # 10 ta xatolikdan keyin admin'ga xabar
                            if error_count >= 10:
                                error_text = f"⚠️ BOT MUAMMOSI!\n\n{error_count} ta xatolik yuz berdi.\n\nOxirgi xatolik: {error_msg}\n\nVaqt: {now.strftime('%H:%M:%S')}\n\n🔧 Bartaraf qilish:\n1. SSH: bash start_bot.sh\n2. Yoki cron job avtomatik tuzatadi (1 daqiqa ichida)"
                                print(error_text)
                                try:
                                    bot_app_temp = ApplicationBuilder().token(BOT_TOKEN).build()
                                    await bot_app_temp.bot.send_message(chat_id=ADMIN_ID, text=error_text)
                                except:
                                    pass
                                error_count = 0  # Reset
            
            if online_on:
                try:
                    if client.is_connected():
                        await client(UpdateStatusRequest(offline=False))
                    else:
                        await client.connect()
                except Exception as e:
                    if "authorization key" not in str(e).lower():
                        print(f"Online xatolik: {e}")
        except Exception as e:
            error_text = f"⚠️ KRITIK XATOLIK!\n\nClock loop to'xtadi: {str(e)}\n\nVaqt: {datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%H:%M:%S')}\n\n🔧 Bartaraf qilish:\n1. SSH: bash start_bot.sh\n2. Yoki cron job avtomatik tuzatadi"
            print(error_text)
            try:
                bot_app_temp = ApplicationBuilder().token(BOT_TOKEN).build()
                await bot_app_temp.bot.send_message(chat_id=ADMIN_ID, text=error_text)
            except:
                pass
            await asyncio.sleep(5)
            continue
        
        # Har sekundda tekshirish (vaqt o'zgarganda darhol yangilanadi)
        await asyncio.sleep(1)
        
        # Har daqiqada animatsiya indeksini oshirish
        if datetime.now(pytz.timezone('Asia/Tashkent')).second == 0:
            animation_index = (animation_index + 1) % len(text_animation)
            await asyncio.sleep(1)  # Bir sekund kutish (takrorlanmaslik uchun)

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("Bot to'xtatildi")
            break
        except Exception as e:
            print(f"Kritik xatolik, qayta ishga tushirilmoqda: {e}")
            import time
            time.sleep(5)
