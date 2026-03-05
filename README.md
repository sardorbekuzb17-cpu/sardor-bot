# Sardor Clock Bot - Telegram Profile Clock

Telegram profilingizda jonli soat va animatsiya ko'rsatadigan bot.

## Xususiyatlar

- ✅ Telegram profilida jonli soat (har daqiqada yangilanadi)
- ✅ "SARDOR" animatsiyasi (har daqiqada bir harf)
- ✅ Qalin yozuv (bold) formatda
- ✅ 24/7 ishlaydi (Alwaysdata scheduled task)
- ✅ Telegram bot bilan boshqarish
- ✅ Veb-panel

## O'rnatish

### 1. Kerakli paketlar

```bash
pip install telethon python-telegram-bot flask pytz aiohttp python-dotenv
```

### 2. Konfiguratsiya

`.env` fayl yarating:

```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
ADMIN_ID=your_telegram_id
WEB_PORT=8080
```

### 3. Session yaratish

```bash
python create_session.py
```

### 4. Botni ishga tushirish

```bash
python main.py
```

## Alwaysdata Deploy

### 1. SSH ulanish

```bash
ssh sardorsoatbot@ssh-sardorsoatbot.alwaysdata.net
```

### 2. Fayllarni yuklash

```bash
scp -r * sardorsoatbot@ssh-sardorsoatbot.alwaysdata.net:~/sardor-clock-bot/
```

### 3. Python 3.10 paketlarni o'rnatish

```bash
/usr/alwaysdata/python/3.10/bin/pip3.10 install --user telethon python-telegram-bot flask pytz aiohttp python-dotenv
```

### 4. Botni ishga tushirish

```bash
cd ~/sardor-clock-bot
nohup /usr/alwaysdata/python/3.10/bin/python3.10 main.py > bot.log 2>&1 &
```

### 5. Scheduled Task sozlash

Alwaysdata panelida:
- Advanced → Scheduled tasks
- Add a scheduled task
- Value: `*/5 * * * *` (har 5 minutda)
- Command: `bash /home/sardorsoatbot/sardor-clock-bot/alwaysdata_restart.sh`

## Fayllar

- `main.py` - Asosiy bot kodi
- `config.py` - Konfiguratsiya
- `create_session.py` - Session yaratish
- `alwaysdata_restart.sh` - Avtomatik restart script
- `requirements.txt` - Python paketlar ro'yxati

## Telegram Bot Buyruqlari

- `/start` - Boshqaruv panelini ochish
- Tugmalar:
  - SOAT ON/OFF - Soatni yoqish/o'chirish
  - ONLINE ON/OFF - Online statusni boshqarish
  - +5s / -5s - Vaqtni sozlash
  - STATISTIKA - Statistikani ko'rish
  - YANGILASH - Panelni yangilash

## Muammolarni hal qilish

### Bot to'xtab qolsa

```bash
ssh sardorsoatbot@ssh-sardorsoatbot.alwaysdata.net
cd sardor-clock-bot
bash alwaysdata_restart.sh
```

### Loglarni ko'rish

```bash
tail -f ~/sardor-clock-bot/bot.log
```

### Session muammosi

```bash
cd ~/sardor-clock-bot
rm -f *.session-journal user_session.session
# Keyin lokal kompyuterdan yangi session yuklang
```

## Muhim Eslatmalar

- ⚠️ Python 3.11 ishlatmang - `_socket` moduli buzilgan
- ✅ Python 3.10 ishlatiladi - barqaror
- ✅ Scheduled task har 5 minutda botni tekshiradi
- ✅ Agar bot to'xtasa, avtomatik qayta ishga tushadi

## Muallif

Sardor - Telegram Clock Bot

## Litsenziya

MIT
