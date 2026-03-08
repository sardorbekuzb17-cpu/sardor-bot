#!/bin/bash

# AlwaysData serveriga ulanish va botni yangilash
echo "Serverga ulanmoqda..."

# SSH orqali faylni yuklash va botni qayta ishga tushirish
scp main.py sardorsoatbot@ssh-sardorsoatbot.alwaysdata.net:~/main.py

# Botni qayta ishga tushirish
ssh sardorsoatbot@ssh-sardorsoatbot.alwaysdata.net << 'EOF'
pkill -f main.py
cd ~/
nohup python3 main.py > bot.log 2>&1 &
echo "Bot qayta ishga tushdi!"
sleep 2
tail -20 bot.log
EOF
