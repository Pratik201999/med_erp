from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.db import Base

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"))
    batch_number = Column(String)
    expiry_date = Column(Date)
    mrp = Column(Float)
    purchase_price = Column(Float)
    quantity = Column(Integer)
    shop_id = Column(Integer, ForeignKey("shops.id"))