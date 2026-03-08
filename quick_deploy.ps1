# Fayllarni serverga yuklash
Write-Host "Fayllarni yuklamoqda..." -ForegroundColor Cyan

scp .env sardorsoatbot@ssh-sardorsoatbot.alwaysdata.net:~/.env
scp config.py sardorsoatbot@ssh-sardorsoatbot.alwaysdata.net:~/config.py

Write-Host "Botni qayta ishga tushirmoqda..." -ForegroundColor Yellow
ssh sardorsoatbot@ssh-sardorsoatbot.alwaysdata.net "pkill -f main.py; sleep 1; cd ~/; nohup python3 main.py > bot.log 2>&1 &"

Start-Sleep -Seconds 3

Write-Host "Loglar:" -ForegroundColor Green
ssh sardorsoatbot@ssh-sardorsoatbot.alwaysdata.net "tail -20 bot.log"
