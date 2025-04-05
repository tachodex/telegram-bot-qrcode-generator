import os
import json
from datetime import datetime
from pyrogram import Client, filters
import qrcode
from io import BytesIO
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Database functions
def load_db():
    try:
        with open('database.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": {}, "stats": {"total_qr_codes": 0, "active_users": 0}}

def save_db(data):
    with open('database.json', 'w') as f:
        json.dump(data, f, indent=2)

def update_user_stats(user_id):
    db = load_db()
    user_id = str(user_id)
    
    if user_id not in db['users']:
        db['users'][user_id] = {
            "qr_count": 0
        }
        db['stats']['active_users'] += 1
    else:
        pass
    
    db['users'][user_id]['qr_count'] += 1
    db['stats']['total_qr_codes'] += 1
    save_db(db)

# Load environment variables
load_dotenv()

# Admin user ID (from .env with hardcoded fallback)
ADMIN_ID = int(os.getenv("ADMIN_ID", "2026106499"))

# Initialize bot
app = Client(
    "qrcode_bot",
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

# Start command
@app.on_message(filters.command("start"))
async def start(client, message):
    # Update user stats on start
    db = load_db()
    user_id = str(message.from_user.id)
    
    if user_id not in db['users']:
        db['users'][user_id] = {
            "qr_count": 0
        }
        db['stats']['active_users'] += 1
        save_db(db)

    await message.reply_text(
        "Welcome to QR Code Bot!\n\n"
        "Available commands:\n"
        "/qr [text] - Generate QR code\n"
        "/usage - View your statistics\n"
        "/clear - Reset your usage data\n\n"
        "Example: /qr https://example.com"
    )

# QR command handler
@app.on_message(filters.command("qr"))
async def qr_handler(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("Please add text after /qr command\nExample: /qr Hello")
            return
            
        text = ' '.join(message.command[1:])
        if len(text) > 1000:
            await message.reply_text("Text too long! Maximum 1000 characters")
            return

        # Generate QR
        qr = qrcode.make(text)
        bio = BytesIO()
        bio.name = 'qr.png'
        qr.save(bio, 'PNG')
        bio.seek(0)
        
        await message.reply_photo(bio, caption="Here's your QR code!")
        update_user_stats(message.from_user.id)
        
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

# Usage command
@app.on_message(filters.command("usage"))
async def usage(client, message):
    db = load_db()
    user_id = str(message.from_user.id)
    
    if user_id in db['users']:
        user = db['users'][user_id]
        await message.reply_text(
            f"📊 Your Usage Stats:\n\n"
            f"QR Codes Generated: {user['qr_count']}"
        )
    else:
        await message.reply_text("You haven't generated any QR codes yet!")

# Clear command
@app.on_message(filters.command("clear"))
async def clear_stats(client, message):
    db = load_db()
    user_id = str(message.from_user.id)
    
    if user_id in db['users']:
        db['users'].pop(user_id)
        db['stats']['active_users'] -= 1
        save_db(db)
        await message.reply_text("Your usage data has been cleared!")
    else:
        await message.reply_text("No data to clear!")

# Stats command (admin only)
@app.on_message(filters.command("stats"))
async def stats(client, message):
    if message.from_user.id != ADMIN_ID:
        await message.reply_text("This command is for admins only!")
        return
        
    db = load_db()
    await message.reply_text(
        f"🤖 Bot Statistics:\n\n"
        f"Total QR Codes Generated: {db['stats']['total_qr_codes']}\n"
        f"Active Users: {db['stats']['active_users']}"
    )

# Handle other messages
@app.on_message(filters.text)
async def text_handler(client, message):
    if not message.text.startswith('/'):
        await message.reply_text(
            "Please use /qr command to generate QR codes\n\n"
            "Available commands:\n"
            "/qr [text] - Generate QR code\n"
            "/usage - View your statistics\n"
            "/clear - Reset your usage data\n"
            "Example: /qr Hello World"
        )

# Flask keepalive
def run_flask():
    flask_app = Flask(__name__)
    @flask_app.route('/')
    def home(): return "Bot is running"
    flask_app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    print("Bot started...")
    app.run()
