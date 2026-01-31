# medical-telegram-warehouse
# Telegram Medical Channel Data Scraper

## Description
Python script to scrape messages and images from Ethiopian medical Telegram channels for data analysis.

## Quick Start

### 1. Get Telegram API Credentials
- Go to https://my.telegram.org
- Create an app to get `API_ID` and `API_HASH`

### 2. Setup Environment
```bash
# Create .env file
echo "API_ID=your_id_here" > .env
echo "API_HASH=your_hash_here" >> .env

# Install dependencies
pip install telethon python-dotenv
 Run: `python src/scraper.py`

## Data Structure
- JSON files: `data/raw/telegram_messages/DATE/channel.json`
- Images: `data/raw/images/channel_name/message_id.jpg`
- Logs: `logs/scraping.log`