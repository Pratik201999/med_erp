from sqlalchemy.orm import Session
from app.models.batch import Batch
from app.models.stock_ledger import StockLedger

def stock_in(db: Session, batch_id: int, quantity: int, ref_type="PURCHASE", ref_id=None):
    if quantity <= 0:
        raise Exception("Quantity must be greater than 0")

    batch = db.query(Batch).filter(Batch.id == batch_id).first()

    if not batch:
        raise Exception("Batch not found")

    try:
        batch.quantity += quantity

        ledger = StockLedger(
            batch_id=batch_id,
            change_type="IN",
            quantity=quantity,
            reference_type=ref_type,
            reference_id=ref_id
        )

        db.add(ledger)
        db.commit()

        return {"message": "Stock added", "new_quantity": batch.quantity}

    except Exception as e:
        db.rollback()
        raise e


def stock_out(db: Session, batch_id: int, quantity: int, ref_type="BILL", ref_id=None):
    if quantity <= 0:
        raise Exception("Quantity must be greater than 0")

    batch = db.query(Batch).filter(Batch.id == batch_id).first()

    if not batch:
        raise Exception("Batch not found")

    if batch.quantity < quantity:
        raise Exception("Insufficient stock")

    try:
        batch.quantity -= quantity

        ledger = StockLedger(
            batch_id=batch_id,
            change_type="OUT",
            quantity=quantity,
            reference_type=ref_type,
            reference_id=ref_id
        )

        db.add(ledger)
        db.commit()

        return {"message": "Stock removed", "remaining_quantity": batch.quantity}

    except Exception as e:
        db.rollback()
        raise e