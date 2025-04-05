# QR Code Telegram Bot 🤖 [Open Source]

A Telegram bot that generates QR codes from text/links. Features usage tracking, admin controls, and simple setup. Built with Python and Pyrogram. Open-source and easy to contribute to!

## 🚀 How to Use

1. Start the bot by sending `/start`
2. Create QR codes with `/qr [your-text]`
   - Example: `/qr https://google.com`
3. Check your usage with `/usage`
4. Clear your data with `/clear`

## 🔧 Setup Guide

1. Get these from [Telegram](https://my.telegram.org/):
   - `API_ID`
   - `API_HASH`
   - `BOT_TOKEN` (from @BotFather)
2. Put them in the `.env` file:
   ```
   API_ID=your_id_here
   API_HASH=your_hash_here
   BOT_TOKEN=your_token_here
   ADMIN_ID=your_admin_id
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```bash
   python telegram_qrcode_gen.py
   ```

## 📊 Features

- Generates QR codes instantly
- Tracks your QR code usage
- Simple admin controls
- Works with text and links

## 👥 Contributing

We welcome contributions! Here's how:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For any issues, please create a [issue](https://github.com/tachodex/telegram-bot-qrcode-generator/issues/new).
