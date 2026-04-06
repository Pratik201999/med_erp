from sqlalchemy import Column, Integer, Float, ForeignKey
from app.db import Base

class BillItem(Base):
    __tablename__ = "bill_items"

    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    batch_id = Column(Integer, ForeignKey("batches.id"))
    quantity = Column(Integer)
    price = Column(Float)
    gst = Column(Float)