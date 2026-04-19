from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials.replace("Bearer ", "")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user = db.query(User).filter(
            User.id == payload["user_id"]
        ).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")