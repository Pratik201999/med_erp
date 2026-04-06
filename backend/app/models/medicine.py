from sqlalchemy import Column, Integer, String
from app.db import Base

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    salt = Column(String)
    category = Column(String)
    schedule_type = Column(String)
    manufacturer = Column(String)