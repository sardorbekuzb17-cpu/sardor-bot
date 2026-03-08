#!/bin/bash
# Bot'ni to'liq sozlash va ishga tushirish

echo "🚀 Bot sozlanmoqda..."

# 1. Scriptlarga ruxsat berish
chmod +x deploy_alwaysdata.sh cron_keepalive.sh

# 2. Eski botni to'xtatish
pkill -f "python3 main.py" 2>/dev/null

# 3. Requirements o'rnatish
pip3 install --user -r requirements.txt

# 4. Botni ishga tushirish
nohup python3 main.py > bot.log 2>&1 &

# 5. Cron job qo'shish
(crontab -l 2>/dev/null | grep -v "cron_keepalive.sh"; echo "*/5 * * * * bash ~/cron_keepalive.sh") | crontab -

echo "✅ Bot ishga tushdi!"
echo "📊 Loglarni ko'rish: tail -f ~/bot.log"
echo "🔄 Cron job qo'shildi: har 5 minutda tekshiradi"

# Tekshirish
sleep 3
if pgrep -f "python3 main.py" > /dev/null; then
    echo "✅ Bot ishlayapti!"
else
    echo "❌ Xatolik! Loglarni tekshiring: cat bot.log"
fi
