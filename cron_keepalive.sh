#!/bin/bash
# Har 5 minutda botni tekshirish va kerak bo'lsa qayta ishga tushirish

cd ~/sardor-clock-bot

# Bot ishlab turganini tekshirish
if ! pgrep -f "python3 main.py" > /dev/null; then
    echo "$(date): Bot to'xtagan, qayta ishga tushirilmoqda..." >> restart.log
    nohup python3 main.py > bot.log 2>&1 &
    echo "$(date): Bot ishga tushirildi" >> restart.log
else
    echo "$(date): Bot ishlayapti" >> keepalive.log
fi
