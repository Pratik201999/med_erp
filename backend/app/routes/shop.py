from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.shop import Shop
from pydantic import BaseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ShopCreate(BaseModel):
    name: str
    gst_number: str
    address: str

@router.post("/")
def create_shop(data: ShopCreate, db: Session = Depends(get_db)):
    shop = Shop(**data.dict())
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop

@router.get("/")
def get_shops(db: Session = Depends(get_db)):
    return db.query(Shop).all()