#!/bin/bash
# Alwaysdata Scheduled Task uchun restart script

cd ~/sardor-clock-bot

# Eski processlarni to'xtatish
pkill -9 -f "python.*main.py" 2>/dev/null

# Session lock tozalash
rm -f *.session-journal

# Botni ishga tushirish (Python 3.10 - barqaror, unbuffered output)
nohup /usr/alwaysdata/python/3.10/bin/python3.10 -u main.py > bot.log 2>&1 &

echo "Bot restarted at $(date)" >> restart.log
