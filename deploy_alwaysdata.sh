#!/bin/bash
# Alwaysdata'ga tezkor deploy

echo "🚀 Alwaysdata'ga deploy boshlanmoqda..."

# Botni to'xtatish
echo "⏹️  Eski botni to'xtatish..."
pkill -f "python3 main.py"
sleep 2

# Yangi versiyani ishga tushirish
echo "▶️  Yangi versiyani ishga tushirish..."
cd ~/sardor-clock-bot
nohup python3 main.py > bot.log 2>&1 &

sleep 3

# Tekshirish
if pgrep -f "python3 main.py" > /dev/null; then
    echo "✅ Bot muvaffaqiyatli ishga tushdi!"
    echo "📊 Loglarni ko'rish: tail -f ~/sardor-clock-bot/bot.log"
else
    echo "❌ Xatolik! Bot ishga tushmadi."
    echo "📋 Loglarni tekshiring: cat ~/sardor-clock-bot/bot.log"
fi
