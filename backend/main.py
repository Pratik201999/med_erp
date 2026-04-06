from fastapi import FastAPI
from app.db import Base, engine
from app.models import *
from app.routes import medicine
from app.routes import batch
from app.routes import inventory
from app.routes import purchase
from app.routes import billing
from app.routes import supplier
from app.routes import shop

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(medicine.router, prefix="/medicines")
app.include_router(batch.router, prefix="/batches")
app.include_router(inventory.router, prefix="/inventory")
app.include_router(purchase.router, prefix="/purchase")
app.include_router(billing.router, prefix="/billing")
app.include_router(supplier.router, prefix="/suppliers")
app.include_router(shop.router, prefix="/shops")

@app.get("/")
def root():
    return {"message": "ERP running 2"}