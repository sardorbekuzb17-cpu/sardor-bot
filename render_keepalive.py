#!/usr/bin/env python3
"""
Render.com da ishlaydigan keepalive service
Har 20 daqiqada Alwaysdata serveriga SSH orqali ulanib botni restart qiladi
"""

import os
import subprocess
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

# SSH ma'lumotlari (Render.com environment variables dan)
SSH_HOST = os.environ.get("SSH_HOST", "ssh-sardorsoatbot.alwaysdata.net")
SSH_USER = os.environ.get("SSH_USER", "sardorsoatbot")
SSH_KEY = os.environ.get("SSH_KEY", "")  # Base64 encoded private key

def setup_ssh_key():
    """SSH key ni fayl sifatida saqlash"""
    if not SSH_KEY:
        print("⚠️ SSH_KEY environment variable yo'q!")
        return None
    
    import base64
    key_path = "/tmp/ssh_key"
    
    try:
        # Base64 dan decode qilish
        key_content = base64.b64decode(SSH_KEY).decode('utf-8')
        
        with open(key_path, 'w') as f:
            f.write(key_content)
        
        # Permissions o'rnatish
        os.chmod(key_path, 0o600)
        print(f"✅ SSH key saqlandi: {key_path}", flush=True)
        return key_path
    except Exception as e:
        print(f"❌ SSH key setup xatosi: {e}")
        return None

def restart_bot():
    """Alwaysdata serverida botni restart qilish"""
    print(f"\n🔄 Bot restart qilinmoqda: {datetime.now()}", flush=True)
    
    key_path = setup_ssh_key()
    if not key_path:
        print("❌ SSH key yo'q, restart bekor qilindi")
        return False
    
    try:
        cmd = [
            "ssh",
            "-i", key_path,
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            f"{SSH_USER}@{SSH_HOST}",
            "cd sardor-clock-bot && bash alwaysdata_restart.sh"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ Bot restart qilindi: {datetime.now()}", flush=True)
            print(f"Output: {result.stdout[:200]}", flush=True)
            return True
        else:
            print(f"⚠️ Restart xatosi (exit code {result.returncode}): {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"❌ SSH xatosi: {e}")
        return False
    finally:
        # SSH key ni o'chirish
        if os.path.exists(key_path):
            os.remove(key_path)

@app.route('/')
def index():
    return jsonify({
        "service": "Sardor Clock Bot Keepalive",
        "status": "running",
        "time": datetime.now().isoformat()
    })

@app.route('/restart')
def restart():
    """Botni restart qilish"""
    success = restart_bot()
    return jsonify({
        "success": success,
        "time": datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

# APScheduler ni Flask app bilan birga ishga tushirish
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(func=restart_bot, trigger="interval", minutes=1)
scheduler.start()

print("🚀 Keepalive service ishga tushdi", flush=True)
print(f"📅 Har 1 daqiqada bot restart qilinadi", flush=True)

# Darhol birinchi restart
restart_bot()
