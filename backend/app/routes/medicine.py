from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.medicine import Medicine

router = APIRouter()

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create medicine
@router.post("/")
def create_medicine(name: str, salt: str, db: Session = Depends(get_db)):
    med = Medicine(name=name, salt=salt)
    db.add(med)
    db.commit()
    db.refresh(med)
    return med

# Get all medicines
@router.get("/")
def get_medicines(db: Session = Depends(get_db)):
    return db.query(Medicine).all()