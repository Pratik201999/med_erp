from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from app.db import Base

class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"))
    medicine_id = Column(Integer, ForeignKey("medicines.id"))
    batch_number = Column(String)
    expiry_date = Column(Date)
    quantity = Column(Integer)
    purchase_price = Column(Float)
    mrp = Column(Float)