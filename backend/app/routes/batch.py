from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.batch import Batch
from pydantic import BaseModel
from datetime import date

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class BatchCreate(BaseModel):
    medicine_id: int
    batch_number: str
    expiry_date: date
    mrp: float
    purchase_price: float
    quantity: int
    shop_id: int

@router.post("/")
def create_batch(data: BatchCreate, db: Session = Depends(get_db)):
    batch = Batch(**data.dict())
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch

@router.get("/")
def get_batches(db: Session = Depends(get_db)):
    return db.query(Batch).all()