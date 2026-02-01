from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductTrend(BaseModel):
    product_name: str
    mention_count: int

class ChannelActivity(BaseModel):
    channel_name: str
    post_count: int
    avg_views: float

class MessageSearchResponse(BaseModel):
    message_id: int
    content: str
    channel_title: str
    view_count: Optional[int]

class VisualStats(BaseModel):
    image_category: str
    total_posts: int
    avg_views: float