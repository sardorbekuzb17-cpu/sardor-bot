#!/bin/bash
pkill -f main.py
sleep 1
nohup python3 main.py > bot.log 2>&1 &
sleep 2
tail -30 bot.log
