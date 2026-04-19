from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.billing_service import create_bill
from pydantic import BaseModel
from typing import List
from app.models.bill import Bill
from app.models.bill_item import BillItem
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/billing", tags=["Billing"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ UPDATED SCHEMA
class BillItemSchema(BaseModel):
    medicine_id: int
    quantity: int
    price: float


class BillSchema(BaseModel):
    discount: float = 0
    payment_mode: str = "CASH"
    items: List[BillItemSchema]


# ✅ CREATE BILL (NO CHANGE NEEDED HERE)
@router.post("/")
def create(
    data: BillSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_bill(
        db,
        current_user.shop_id,
        [i.dict() for i in data.items],
        data.discount,
        data.payment_mode
    )


# ✅ GET ALL BILLS
@router.get("/")
def get_bills(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Bill).filter(
        Bill.shop_id == current_user.shop_id
    ).all()


# ✅ GET ALL ITEMS
@router.get("/items")
def get_all_items(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(BillItem).join(Bill).filter(
        Bill.shop_id == current_user.shop_id
    ).all()


# ✅ GET ITEMS BY BILL
@router.get("/items/{bill_id}")
def get_items_by_bill(
    bill_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    bill = db.query(Bill).filter(
        Bill.id == bill_id,
        Bill.shop_id == current_user.shop_id
    ).first()

    if not bill:
        return {"error": "Unauthorized or Bill not found"}

    return db.query(BillItem).filter(
        BillItem.bill_id == bill_id
    ).all()


# ✅ GET SINGLE BILL
@router.get("/{bill_id}")
def get_bill(
    bill_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    bill = db.query(Bill).filter(
        Bill.id == bill_id,
        Bill.shop_id == current_user.shop_id
    ).first()

    if not bill:
        return {"error": "Unauthorized or Bill not found"}

    items = db.query(BillItem).filter(
        BillItem.bill_id == bill_id
    ).all()

    return {
        "bill": bill,
        "items": items
    }