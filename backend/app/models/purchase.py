from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from app.db import Base
from datetime import datetime

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    shop_id = Column(Integer, ForeignKey("shops.id"))
    total_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)