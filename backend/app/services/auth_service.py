from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token


def signup(db: Session, data: dict):
    existing_user = db.query(User).filter(User.username == data["username"]).first()
    if existing_user:
        raise Exception("Username already exists")

    user = User(
        username=data["username"],
        password=hash_password(data["password"]),
        role=data["role"],
        shop_id=data["shop_id"]
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return create_access_token({
        "user_id": user.id,
        "shop_id": user.shop_id,
        "role": user.role
    })


def login(db: Session, data: dict):
    user = db.query(User).filter(User.username == data["username"]).first()

    if not user or not verify_password(data["password"], user.password):
        raise Exception("Invalid credentials")

    return create_access_token({
        "user_id": user.id,
        "shop_id": user.shop_id,
        "role": user.role
    })