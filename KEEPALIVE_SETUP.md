# Bot Doimiy Ishlashi Uchun Yechim

## Muammo

Alwaysdata bepul rejada processlar 24 soatdan keyin to'xtaydi.

## Yechim: Tashqi Monitoring

### Variant 1: UptimeRobot (Tavsiya etiladi - 100% bepul)

1. **UptimeRobot.com** ga kiring
2. **Add New Monitor** bosing
3. Quyidagilarni to'ldiring:
   - Monitor Type: `HTTP(s)`
   - Friendly Name: `Sardor Bot`
   - URL: `http://185.31.41.85:8080`
   - Monitoring Interval: `5 minutes`
4. **Create Monitor** bosing

UptimeRobot har 5 minutda botga ping yuboradi va bot ishlab turadi.

### Variant 2: Cron-job.org (Bepul)

1. **cron-job.org** ga kiring
2. **Create cronjob** bosing
3. Quyidagilarni to'ldiring:
   - Title: `Sardor Bot Keepalive`
   - URL: `http://185.31.41.85:8080`
   - Execution schedule: `Every 5 minutes`
4. **Create cronjob** bosing

### Variant 3: PythonAnywhere (Bepul, eng ishonchli)

1. **pythonanywhere.com** ga ro'yxatdan o'ting
2. **Files** → **Upload a file** → `external_keepalive.py` ni yuklang
3. **Consoles** → **Bash** oching
4. Quyidagi buyruqlarni bajaring:

   ```bash
   pip3 install --user requests
   nohup python3 external_keepalive.py > keepalive.log 2>&1 &
   ```

5. Loglarni ko'rish:

   ```bash
   tail -f keepalive.log
   ```

### Variant 4: Render.com (Bepul)

1. **render.com** ga kiring
2. **New** → **Background Worker**
3. GitHub repo'ni ulang
4. **Start Command:** `python3 external_keepalive.py`
5. **Create Background Worker**

## Qo'shimcha: Telegram Bot Webhook (Eng yaxshi yechim)

Polling o'rniga webhook ishlatish - bu eng ishonchli yechim.

### Webhook sozlash

1. `main.py` ni webhook rejimiga o'tkazish
2. Telegram webhook URL: `https://your-domain.com/webhook`
3. Webhook avtomatik ishga tushadi, polling kerak emas

## Xulosa

**Eng oson:** UptimeRobot (5 minut sozlash)
**Eng ishonchli:** PythonAnywhere + external_keepalive.py
**Eng professional:** Webhook rejimi

## Hozirgi holat

✅ Bot ishga tushdi
✅ Auto-restart har 12 soatda
✅ Keepalive har 2 minutda
⚠️ Tashqi monitoring kerak (yuqoridagi variantlardan birini tanlang)
