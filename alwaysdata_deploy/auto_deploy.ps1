# Alwaysdata'ga avtomatik deploy
# Faqat bir marta parol kiriting

Write-Host "🚀 Alwaysdata'ga deploy boshlanmoqda..." -ForegroundColor Green

$commands = @"
chmod +x deploy_alwaysdata.sh cron_keepalive.sh setup_bot.sh
pkill -f 'python3 main.py'
pip3 install --user -r requirements.txt
nohup python3 main.py > bot.log 2>&1 &
(crontab -l 2>/dev/null | grep -v 'cron_keepalive.sh'; echo '*/5 * * * * bash ~/cron_keepalive.sh') | crontab -
sleep 3
echo '✅ Bot ishga tushdi!'
ps aux | grep 'python3 main.py' | grep -v grep
tail -5 bot.log
"@

Write-Host "`n📝 Quyidagi buyruqlar bajariladi:" -ForegroundColor Yellow
Write-Host $commands -ForegroundColor Cyan

Write-Host "`n🔐 Iltimos, Alwaysdata parolingizni kiriting..." -ForegroundColor Yellow

# SSH ulanish
ssh sardorsoatbot@ssh-sardorsoatbot.alwaysdata.net $commands

Write-Host "`n✅ Deploy tugadi!" -ForegroundColor Green
