import os
import json
from datetime import datetime
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto

# Load .env credentials
load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

# Telegram channels to scrape
channels = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma",
    "https://t.me/doctorsonlineet"
    # Add more if needed
]

# Output path setup
today = datetime.now().strftime("%Y-%m-%d")
output_base = f"data/raw/telegram_messages/{today}"
os.makedirs(output_base, exist_ok=True)

# Connect to Telegram
client = TelegramClient("scraper_session", api_id, api_hash)

async def scrape_channel(channel_url):
    await client.start()
    channel_name = channel_url.split("/")[-1]
    messages = []

    print(f"🔍 Scraping channel: {channel_name}")

    async for message in client.iter_messages(channel_url, limit=100):
        msg_data = {
            "id": message.id,
            "date": str(message.date),
            "message": message.message,
            "has_media": bool(message.media),
            "media_type": "photo" if isinstance(message.media, MessageMediaPhoto) else None,
        }

        # Save photo separately
        if isinstance(message.media, MessageMediaPhoto):
            img_dir = f"data/raw/images/{channel_name}"
            os.makedirs(img_dir, exist_ok=True)
            try:
                await message.download_media(file=img_dir)
            except Exception as e:
                print(f"❌ Failed to download image: {e}")

        messages.append(msg_data)

    with open(f"{output_base}/{channel_name}.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(messages)} messages from {channel_name}")

# Run for all channels
with client:
    for channel in channels:
        client.loop.run_until_complete(scrape_channel(channel))
