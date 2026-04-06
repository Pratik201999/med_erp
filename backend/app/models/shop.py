from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base
from datetime import datetime

class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gst_number = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)