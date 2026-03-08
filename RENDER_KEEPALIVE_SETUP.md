# Render.com Keepalive Setup

Bu service Alwaysdata botini 24/7 ishlatish uchun - har 20 daqiqada SSH orqali restart qiladi.

## 1. SSH Key ni Base64 ga encode qilish

Windows PowerShell:
```powershell
$keyContent = Get-Content "$env:USERPROFILE\.ssh\id_rsa_alwaysdata" -Raw
$bytes = [System.Text.Encoding]::UTF8.GetBytes($keyContent)
$base64 = [Convert]::ToBase64String($bytes)
$base64 | Set-Clipboard
Write-Host "SSH key clipboard ga ko'chirildi!"
```

## 2. Render.com da Web Service yaratish

1. https://render.com ga kiring (GitHub bilan)
2. **New +** > **Web Service**
3. Repository tanlang: `sardor-clock-bot`
4. Settings:
   - **Name**: `sardor-bot-keepalive`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r render_requirements.txt`
   - **Start Command**: `gunicorn render_keepalive:app`
   - **Instance Type**: `Free`

## 3. Environment Variables qo'shish

**Environment** bo'limida:

```
SSH_HOST = ssh-sardorsoatbot.alwaysdata.net
SSH_USER = sardorsoatbot
SSH_KEY = [clipboard dan paste qiling - Base64 encoded key]
```

## 4. Deploy qilish

**Create Web Service** tugmasini bosing. Render.com avtomatik deploy qiladi.

## 5. Tekshirish

Deploy tugagach:
- Service URL ni oching (masalan: `https://sardor-bot-keepalive.onrender.com`)
- `/restart` endpoint ga boring - bot restart bo'lishi kerak
- Loglarni ko'ring: **Logs** bo'limida

## 6. Ishlash printsipi

- Render.com service 24/7 ishlaydi (free tier)
- Har 20 daqiqada Alwaysdata serveriga SSH orqali ulanadi
- `alwaysdata_restart.sh` scriptni ishga tushiradi
- Bot restart bo'ladi va 24 soat limiti reset bo'ladi

## 7. Monitoring

Render.com loglarida ko'rasiz:
```
✅ Bot restart qilindi: 2026-03-08 20:00:00
✅ Bot restart qilindi: 2026-03-08 20:20:00
✅ Bot restart qilindi: 2026-03-08 20:40:00
```

## Muqobil variant: Railway.app

Agar Render.com ishlamasa, Railway.app ishlatishingiz mumkin (xuddi shu setup).

## Muqobil variant 2: Fly.io

Fly.io ham bepul tier beradi va SSH qo'llab-quvvatlaydi.
