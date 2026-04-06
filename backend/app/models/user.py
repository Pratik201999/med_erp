from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    shop_id = Column(Integer, ForeignKey("shops.id"))