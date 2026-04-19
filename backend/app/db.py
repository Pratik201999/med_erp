# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql://postgres:admin@localhost:5432/medical_erp"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Switch to SQLite
DATABASE_URL = "sqlite:///./mederp.db"

# SQLite needs this extra config
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()