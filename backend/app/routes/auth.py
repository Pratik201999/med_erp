from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.auth_service import signup, login

router = APIRouter(prefix="/auth", tags=["Auth"])

from pydantic import BaseModel

class SignupRequest(BaseModel):
    username: str
    password: str
    role: str
    shop_id: int

class LoginRequest(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @router.post("/signup")
# async def signup_api(request: Request, db: Session = Depends(get_db)):
#     data = await request.json()
#     token = signup(db, data)
#     return {"access_token": token}

@router.post("/signup")
def signup_api(data: SignupRequest, db: Session = Depends(get_db)):
    token = signup(db, data.dict())
    return {"access_token": token}


# @router.post("/login")
# async def login_api(request: Request, db: Session = Depends(get_db)):
#     data = await request.json()
#     token = login(db, data)
#     return {"access_token": token}

@router.post("/login")
def login_api(data: LoginRequest, db: Session = Depends(get_db)):
    token = login(db, data.dict())
    return {"access_token": token}