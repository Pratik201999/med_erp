from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db import Base
from datetime import datetime

class StockLedger(Base):
    __tablename__ = "stock_ledger"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey("batches.id"))
    change_type = Column(String)  # IN / OUT / ADJUST
    quantity = Column(Integer)
    reference_type = Column(String)  # PURCHASE / BILL
    reference_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)