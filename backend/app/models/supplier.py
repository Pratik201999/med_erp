from sqlalchemy import Column, Integer, String
from app.db import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact = Column(String)