#!/bin/bash
# Alwaysdata'ga tezkor deploy

echo "🚀 Alwaysdata'ga deploy boshlanmoqda..."

# Botni to'xtatish
echo "⏹️  Eski botni to'xtatish..."
pkill -f "python3.*main.py"
sleep 2

# Yangi versiyani ishga tushirish
echo "▶️  Yangi versiyani ishga tushirish..."
cd ~/sardor-clock-bot || exit 1
nohup python3 -u main.py > bot.log 2>&1 </dev/null &
BOTPID=$!

sleep 5

# Tekshirish
if ps -p $BOTPID > /dev/null 2>&1; then
    echo "✅ Bot muvaffaqiyatli ishga tushdi! (PID: $BOTPID)"
    echo "📊 Loglarni ko'rish: tail -f ~/sardor-clock-bot/bot.log"
    tail -10 bot.log
else
    echo "❌ Xatolik! Bot ishga tushmadi."
    echo "📋 Loglar:"
    cat bot.log
fi
