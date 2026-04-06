from sqlalchemy.orm import Session
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.batch import Batch
from app.services.inventory_service import stock_in

def create_purchase(db: Session, supplier_id, shop_id, items):
    purchase = Purchase(
        supplier_id=supplier_id,
        shop_id=shop_id,
        total_amount=0
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    total = 0

    for item in items:
        # Save purchase item
        purchase_item = PurchaseItem(
            purchase_id=purchase.id,
            **item
        )
        db.add(purchase_item)

        # Create batch
        batch = Batch(
            medicine_id=item["medicine_id"],
            batch_number=item["batch_number"],
            expiry_date=item["expiry_date"],
            mrp=item["mrp"],
            purchase_price=item["purchase_price"],
            quantity=0,
            shop_id=shop_id
        )
        db.add(batch)
        db.commit()
        db.refresh(batch)

        # Add stock (ledger-based)
        stock_in(db, batch.id, item["quantity"], "PURCHASE", purchase.id)

        total += item["quantity"] * item["purchase_price"]

    purchase.total_amount = total
    db.commit()

    return purchase