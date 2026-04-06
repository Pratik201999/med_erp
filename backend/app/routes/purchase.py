from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.purchase_service import create_purchase
from pydantic import BaseModel
from typing import List
from datetime import date

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PurchaseItemSchema(BaseModel):
    medicine_id: int
    batch_number: str
    expiry_date: date
    quantity: int
    purchase_price: float
    mrp: float

class PurchaseSchema(BaseModel):
    supplier_id: int
    shop_id: int
    items: List[PurchaseItemSchema]

@router.post("/")
def create(data: PurchaseSchema, db: Session = Depends(get_db)):
    return create_purchase(db, data.supplier_id, data.shop_id, [i.dict() for i in data.items])