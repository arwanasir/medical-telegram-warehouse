# Medical Telegram Warehouse

A data engineering and analytics project for collecting, structuring, and analyzing content from Ethiopian medical Telegram channels. The repository combines message scraping, warehouse-style transformation, computer vision enrichment, and a FastAPI analytics layer.

## Overview

This project turns raw Telegram channel content into an analysis-ready dataset. It is designed as a multi-stage pipeline:

- scrape messages and images from Telegram medical channels
- load and structure the collected data
- transform raw content into warehouse-friendly models
- enrich image data with object detection outputs
- expose selected metrics through an API layer

The result is a repository that spans data collection, transformation, machine learning enrichment, and downstream analytical access.

## Repository Structure

```text
medical-telegram-warehouse/
├── api/                       # FastAPI analytics service
├── medical_warehouse/         # dbt project for transformations and marts
├── notebooks/                 # Analysis and experimentation notebooks
├── src/
│   ├── scraper.py             # Telegram collection workflow
│   ├── database_load.py       # Database ingestion utilities
│   ├── yolo_detect.py         # YOLO-based image categorization
│   └── upload_yolo.py         # Detection upload helper
├── orchestration.py           # High-level pipeline coordination
└── requirements.txt           # Python dependencies
```

## Core Components

- `src/scraper.py`: pulls messages and images from Telegram channels
- `src/database_load.py`: prepares and loads collected data into the database layer
- `medical_warehouse/`: dbt models for staging and mart-style transformation
- `src/yolo_detect.py`: image categorization using YOLO
- `api/main.py`: FastAPI service for querying analytical outputs such as top products, channel activity, and visual content statistics

## Tech Stack

- Python
- Telethon
- Pandas and NumPy
- PostgreSQL and SQLAlchemy
- dbt
- YOLO / Ultralytics
- FastAPI

## What This Project Demonstrates

- data ingestion from an external messaging platform
- transformation of semi-structured data into warehouse-ready models
- enrichment of text-and-image datasets with computer vision outputs
- exposure of analytical results through API endpoints
- end-to-end thinking across data engineering, analytics, and ML-assisted processing

## Getting Started

### 1. Create your environment file

Add your Telegram credentials to a local `.env` file:

```env
API_ID=your_api_id
API_HASH=your_api_hash
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run scraping

```bash
python src/scraper.py
```

### 4. Load data into the database workflow

```bash
python src/database_load.py
```

### 5. Run warehouse transformations

```bash
dbt run --project-dir medical_warehouse
```

### 6. Run image detection

```bash
python src/yolo_detect.py
```

### 7. Start the analytics API

```bash
uvicorn api.main:app --reload
```

## Example API Use Cases

The FastAPI service exposes endpoints for questions such as:

- which products or terms appear most frequently in the scraped messages?
- how active is a specific channel and what level of engagement does it get?
- what image categories are most common after YOLO enrichment?
- which messages contain a given medical keyword?

## Notes

This repository is strongest as a pipeline and analytics project. Some infrastructure files exist as scaffolding, but the core value of the repo is the end-to-end workflow from Telegram ingestion to transformed analytical outputs and API access.
