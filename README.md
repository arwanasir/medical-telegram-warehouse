# medical-telegram-warehouse
## Telegram Medical Channel Data Scraper

## Description
This repository contains a data pipeline for medical image analysis. It automates the process of transforming raw Telegram data into a structured warehouse and applying computer vision to categorize content.
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
- Logs: `logs/scraping.log`,
---

Task 2: Data Modeling & Transformation (dbt)
- The goal of this task was to structure raw data into a clean, analytics-ready format using dbt and PostgreSQL.

- Staging Layer: Cleaned and cast raw types from Telegram scrapes to ensure data integrity.

- Marts Layer: Developed the fct_messages model to track key business metrics like view counts and engagement.

- Documentation: Generated a comprehensive lineage graph and schema documentation for full pipeline transparency.

 Task 3: Object Detection (YOLOv8)
- Applied AI to the images collected in Task 1 to extract visual insights and categorize channel content.

- Detection Script: Created src/yolo_detect.py using the YOLOv8 nano model for efficient local processing.

- Classification Scheme:

- promotional: Image contains both a person and a product.

- product_display: Image contains products only (bottles, containers).

- lifestyle: Image contains people only.

- other: Neither specific medical objects nor people detected.

- Integration: YOLO results are joined back to the dbt warehouse in the fct_image_detections model to correlate visual content with performance metrics.

-  Project Structure

├── data/raw/images/      # Source images from Task 1
├── medical_warehouse/    # dbt project folder
│   ├── models/           # SQL transformation logic (Staging & Marts)
│   └── target/           # Compiled documentation and metadata
├── src/
│   └── yolo_detect.py    # AI Detection script
└── yolo_results.csv      # Exported detection data for database loading

- Setup & Execution
- Transform Data:


Run: `dbt run`

Run AI Detection:
Run: `python src/yolo_detect.py`

Generate & View Documentation:
Run:`dbt docs generate && dbt docs serve`