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

## Filename Display

When a file is saved, and whenever an existing file is returned by search, the
bot replaces the final filename component before its extension with `infinity`
and separates components with dots. For example,
`a_bbs_primexofficial.mkv`, `a bbs primexofficial.mkv`, and
`a.bbs.primexofficial.mp4` become `a.bbs.infinity.mkv` or
`a.bbs.infinity.mp4`. Existing database records are normalized when read;
Telegram's cached download keeps the original uploaded filename.

## Title Requests

In a private chat with the bot, users can submit a missing title with `/request Title`
and check their latest requests with `/myrequests`. Admins can review pending requests
with `/requests [page]` and mark one fulfilled with `/fulfill <request ID>`. The bot
notifies the requester when an admin marks a request fulfilled. The existing group
`/request` reporting command remains available and continues to use `REQST_CHANNEL`.
