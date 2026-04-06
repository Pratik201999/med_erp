from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.billing_service import create_bill
from pydantic import BaseModel
from typing import List
from app.models.bill import Bill
from app.models.bill_item import BillItem

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class BillItemSchema(BaseModel):
    batch_id: int
    quantity: int
    price: float

class BillSchema(BaseModel):
    shop_id: int
    discount: float = 0
    payment_mode: str = "CASH"
    items: List[BillItemSchema]

@router.post("/")
def create(data: BillSchema, db: Session = Depends(get_db)):
    return create_bill(db, data.shop_id, [i.dict() for i in data.items], data.discount, data.payment_mode)

@router.get("/")
def get_bills(db: Session = Depends(get_db)):
    return db.query(Bill).all()

@router.get("/items")
def get_all_items(db: Session = Depends(get_db)):
    return db.query(BillItem).all()

@router.get("/items/{bill_id}")
def get_items_by_bill(bill_id: int, db: Session = Depends(get_db)):
    items = db.query(BillItem).filter(BillItem.bill_id == bill_id).all()

    if not items:
        return {"message": "No items found for this bill"}

    return items

@router.get("/{bill_id}")
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(Bill.id == bill_id).first()

    if not bill:
        return {"error": "Bill not found"}

    items = db.query(BillItem).filter(BillItem.bill_id == bill_id).all()

    return {
        "bill": bill,
        "items": items
    }