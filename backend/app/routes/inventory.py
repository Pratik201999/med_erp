from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.inventory_service import stock_in, stock_out
from pydantic import BaseModel
from app.models.stock_ledger import StockLedger
from app.models.batch import Batch

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class StockRequest(BaseModel):
    batch_id: int
    quantity: int

@router.post("/in")
def add_stock(data: StockRequest, db: Session = Depends(get_db)):
    return stock_in(db, data.batch_id, data.quantity)

@router.post("/out")
def remove_stock(data: StockRequest, db: Session = Depends(get_db)):
    return stock_out(db, data.batch_id, data.quantity)

@router.get("/ledger/{batch_id}")
def get_ledger(batch_id: int, db: Session = Depends(get_db)):
    return db.query(StockLedger).filter(StockLedger.batch_id == batch_id).all()


@router.get("/stock/{batch_id}")
def get_stock(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    return {
        "batch_id": batch_id,
        "quantity": batch.quantity
    }