# Alwaysdata'ga Deploy Qilish

## 1. SSH orqali ulanish

```bash
ssh sardorsoatbot@ssh-sardorsoatbot.alwaysdata.net
```

## 2. Yangilangan fayllarni yuklash

### Variant A: Git orqali (tavsiya etiladi)

```bash
cd ~/sardor-clock-bot
git pull origin main
```

### Variant B: FTP/SFTP orqali

- FileZilla yoki WinSCP ishlatib quyidagi fayllarni yuklang:
  - main.py
  - config.py
  - cron_keepalive.sh
  - keep_alive.sh

## 3. Botni qayta ishga tushirish

```bash
cd ~/sardor-clock-bot

# Eski botni to'xtatish
pkill -f "python3 main.py"

# Yangi versiyani ishga tushirish
nohup python3 main.py > bot.log 2>&1 &

# Tekshirish
ps aux | grep main.py
tail -f bot.log
```

## 4. Cron Job o'rnatish (muhim!)

Alwaysdata dashboard'ga kiring:

1. "Scheduled tasks" bo'limiga o'ting
2. "Add a scheduled task" bosing
3. Quyidagilarni kiriting:
   - Command: `bash ~/sardor-clock-bot/cron_keepalive.sh`
   - Frequency: `*/5 * * * *` (har 5 minutda)
   - Enable: ✓

Yoki SSH orqali:

```bash
crontab -e

# Quyidagi qatorni qo'shing:
*/5 * * * * bash ~/sardor-clock-bot/cron_keepalive.sh
```

## 5. Loglarni ko'rish

```bash
# Bot loglari
tail -f ~/sardor-clock-bot/bot.log

# Restart loglari
tail -f ~/sardor-clock-bot/restart.log

# Keepalive loglari
tail -f ~/sardor-clock-bot/keepalive.log
```

## Muammolarni bartaraf qilish

### Bot ishlamayapti

```bash
cd ~/sardor-clock-bot
python3 main.py
# Xatoliklarni ko'ring
```

### Session muammosi

```bash
cd ~/sardor-clock-bot
rm -f user_session.session
python3 create_session.py
# Telefon raqam va kodni kiriting
```

### Cron ishlamayapti

```bash
# Cron loglarini tekshirish
crontab -l
grep CRON /var/log/syslog
```
