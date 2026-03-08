# AlwaysData serveriga faylni yuklash va botni qayta ishga tushirish

Write-Host "Faylni serverga yuklamoqda..." -ForegroundColor Green

# SCP orqali fayl yuklash
scp main.py sardorsoatbot@ssh-sardorsoatbot.alwaysdata.net:~/main.py

# SSH orqali botni qayta ishga tushirish
ssh sardorsoatbot@ssh-sardorsoatbot.alwaysdata.net "pkill -f main.py; cd ~/; nohup python3 main.py > bot.log 2>&1 & sleep 2; tail -20 bot.log"

Write-Host "Tayyor!" -ForegroundColor Green
