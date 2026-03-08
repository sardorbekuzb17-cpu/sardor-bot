#!/bin/bash
# Bot ishlab turganini tekshirish va kerak bo'lsa qayta ishga tushirish

if ! pgrep -f "python3 main.py" > /dev/null; then
    cd /home/sardorsoatbot
    nohup python3 main.py > bot.log 2>&1 &
    echo "$(date): Bot qayta ishga tushirildi" >> restart.log
fi
