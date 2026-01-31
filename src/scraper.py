import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto

# Load credentials from .env
load_dotenv()
API_ID = os.getenv('TG_API_ID')
API_HASH = os.getenv('TG_API_HASH')
PHONE = os.getenv('PHONE')

# Set up logging as required in Task 1
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='../logs/scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class TelegramScraper:
    def __init__(self):
        api_id = os.getenv('TG_API_ID')
        api_hash = os.getenv('TG_API_HASH')

        if not api_id or not api_hash:
            raise ValueError(
                "API_ID or API_HASH is missing from environment variables!")

        self.client = TelegramClient('scraping_session', int(api_id), api_hash)

    async def start(self):
        await self.client.start(PHONE)

    async def scrape_channel(self, channel_username, limit=100):
        """Scrapes messages and images, saving them in a partitioned structure."""
        try:
            entity = await self.client.get_entity(channel_username)
            messages_data = []

            # Directory for images: data/raw/images/{channel_name}/
            image_dir = f"../data/raw/images/{channel_username}"
            os.makedirs(image_dir, exist_ok=True)

            async for message in self.client.iter_messages(entity, limit=limit):
                # Extract fields required by Task 1 [cite: 127-129]
                msg_info = {
                    "message_id": message.id,
                    "channel_name": channel_username,
                    "message_date": message.date.isoformat(),
                    "message_text": message.text,
                    "has_media": message.media is not None,
                    "image_path": None,
                    "views": getattr(message, 'views', 0),
                    "forwards": getattr(message, 'forwards', 0)
                }

                # Download images if present [cite: 131]
                if isinstance(message.media, MessageMediaPhoto):
                    img_path = await message.download_media(file=f"{image_dir}/{message.id}.jpg")
                    msg_info["image_path"] = img_path

                messages_data.append(msg_info)

            # Save JSON in partitioned format: YYYY-MM-DD/channel.json
            date_str = datetime.now().strftime("%Y-%m-%d")
            output_dir = f"../data/raw/telegram_messages/{date_str}"
            os.makedirs(output_dir, exist_ok=True)

            with open(f"{output_dir}/{channel_username}.json", 'w', encoding='utf-8') as f:
                json.dump(messages_data, f, indent=4, ensure_ascii=False)

            logging.info(
                f"Successfully scraped {len(messages_data)} messages from {channel_username}")
            return messages_data

        except Exception as e:
            logging.error(f"Error scraping {channel_username}: {str(e)}")
            print(f"Error: {e}")

    async def disconnect(self):
        await self.client.disconnect()
