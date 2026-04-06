from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from app.db import Base
from datetime import datetime

class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, ForeignKey("shops.id"))
    total_amount = Column(Float)
    discount = Column(Float)
    gst_amount = Column(Float)
    payment_mode = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)