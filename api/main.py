from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from . import models, schemas, database

app = FastAPI(title="Medical Warehouse API", description="Analytical API for Telegram Data")


@app.get("/api/reports/top-products",tags=["Analytics"], response_model=List[schemas.ProductTrend])
def get_top_products(limit: int = 10, db: Session = Depends(database.get_db)):
    """
    Returns the most frequently mentioned medical terms/products.
    Note: In a production environment, this would query a dedicated 'dim_products' table.
    """
    
    results = db.query(
        models.Message.content.label("product_name"),
        func.count(models.Message.message_id).label("mention_count")
    ).filter(models.Message.content != None) \
     .group_by(models.Message.content) \
     .order_by(func.count(models.Message.message_id).desc()) \
     .limit(limit).all()
    return results


@app.get(
    "/api/channels/{channel_name}/activity", 
    response_model=schemas.ChannelActivity,
    summary="Channel Performance Trends",
    description="Get posting volume and engagement metrics (average views) for a specific Telegram channel."
)
def get_channel_activity(channel_name: str, db: Session = Depends(database.get_db)):
    result = db.query(
        models.Message.channel_title.label("channel_name"),
        func.count(models.Message.message_id).label("post_count"),
        func.avg(models.Message.view_count).label("avg_views")
    ).filter(models.Message.channel_title.ilike(f"%{channel_name}%")) \
     .group_by(models.Message.channel_title).first()
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Channel '{channel_name}' not found")
    return result


@app.get(
    "/api/search/messages", 
    response_model=List[schemas.MessageSearchResponse],
    tags=["Search"],
    summary="Search Telegram Messages",
    description="Performs a case-insensitive search through all scraped messages to find specific medical keywords or phrases."
)
def search_messages(
    query: str = Query(..., description="The word or drug name you want to find (e.g., 'Paracetamol')"), 
    limit: int = Query(20, description="The maximum number of messages to return"), 
    db: Session = Depends(database.get_db)
):
    results = db.query(models.Message).filter(
        models.Message.content.ilike(f"%{query}%")
    ).limit(limit).all()
    return results


@app.get(
    "/api/reports/visual-content", 
    response_model=List[schemas.VisualStats],
    tags=["Analytics"],
    summary="Get AI Image Statistics",
    description="Returns a summary of images detected by YOLOv8, grouped by category (Promotional, Lifestyle, etc.) with average view counts."
)
def get_visual_stats(db: Session = Depends(database.get_db)):
    return db.query(
        models.ImageDetection.image_category,
        func.count(models.ImageDetection.message_id).label("total_posts"),
        func.avg(models.ImageDetection.view_count).label("avg_views")
    ).group_by(models.ImageDetection.image_category).all()
@app.get(
    "/health", 
    summary="API Health Status", 
    tags=["System"],
    description="Check if the API and database connection are operational."
)
def health_check():
    return {"status": "healthy"}