#!/bin/bash
pkill -9 -f 'python.*main.py'
sleep 3
cd ~
nohup python3 main.py > bot.log 2>&1 &
echo "Bot ishga tushdi!"
sleep 3
tail -30 bot.log
