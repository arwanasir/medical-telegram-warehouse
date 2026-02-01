from sqlalchemy import Column, BigInteger, Text, Integer, Float, DateTime
from .database import Base

class Message(Base):
    __tablename__ = "fact_messages"
    __table_args__ = {"extend_existing": True}

    message_id = Column(BigInteger, primary_key=True)
    channel_title = Column(Text)
    content = Column(Text)
    view_count = Column(Integer)
    date_key = Column(DateTime) 

class ImageDetection(Base):
    __tablename__ = "fct_image_detections"
    __table_args__ = {"extend_existing": True}

    message_id = Column(BigInteger, primary_key=True)
    image_category = Column(Text)
    view_count = Column(Integer)