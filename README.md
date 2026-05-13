# 🌱 Poppy Seeds Bot

An Advanced Auto Filter Bot with amazing features.

**Join our channel: [@letswatchitnow](https://t.me/letswatchitnow)**

## Required Variables

- `BOT_TOKEN` - Get from [@BotFather](https://t.me/BotFather)
- `API_ID` - Get from [my.telegram.org](https://my.telegram.org)
- `API_HASH` - Get from [my.telegram.org](https://my.telegram.org)
- `CHANNELS` - Your DB channel ID (where you upload files)
- `ADMINS` - Your Telegram user ID
- `DATABASE_URI` - MongoDB connection string
- `LOG_CHANNEL` - A channel ID for bot logs

## Optional Variables

- `AUTH_CHANNEL` - Force subscribe channel ID
- `PICS` - Start message photo URL
- `SUPPORT_CHAT` - Support group username
- `AUTO_DELETE` - Auto delete files after sending (True/False)
- `IMDB` - Show IMDB info (True/False)
- `PROTECT_CONTENT` - Prevent forwarding (True/False)

## Deploy on VPS

```bash
git clone <your-repo>
pip3 install -r requirements.txt
# Fill in your values in info.py or set as environment variables
python3 bot.py
```

## How to Use

1. Add bot as admin to your DB channel
2. Upload movie files to DB channel
3. Add bot to your group
4. Users search by typing movie names
