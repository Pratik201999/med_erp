from sqlalchemy.orm import Session
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.batch import Batch
from app.services.inventory_service import stock_in


def create_purchase(db: Session, supplier_id, shop_id, items):
    try:
        total = 0

        # 🧾 Create purchase (NO COMMIT)
        purchase = Purchase(
            supplier_id=supplier_id,
            shop_id=shop_id,
            total_amount=0
        )
        db.add(purchase)
        db.flush()  # ✅ get purchase.id

        for item in items:

            if item["quantity"] <= 0:
                raise Exception("Invalid quantity")

            # 🧠 Create batch
            batch = Batch(
                medicine_id=item["medicine_id"],
                batch_number=item["batch_number"],
                expiry_date=item["expiry_date"],
                mrp=item["mrp"],
                purchase_price=item["purchase_price"],
                quantity=0,  # will be updated via stock_in
                shop_id=shop_id
            )

            db.add(batch)
            db.flush()  # ✅ get batch.id

            # 📈 Add stock (NO COMMIT inside)
            stock_in(
                db,
                batch_id=batch.id,
                quantity=item["quantity"],
                ref_type="PURCHASE",
                ref_id=purchase.id
            )

            # 🧾 Create PurchaseItem (NO batch_id here)
            purchase_item = PurchaseItem(
                purchase_id=purchase.id,
                medicine_id=item["medicine_id"],
                batch_number=item["batch_number"],
                expiry_date=item["expiry_date"],
                quantity=item["quantity"],
                purchase_price=item["purchase_price"],
                mrp=item["mrp"]
            )

            db.add(purchase_item)

            # 💰 Calculate total
            total += item["quantity"] * item["purchase_price"]

        purchase.total_amount = total

        # ✅ SINGLE COMMIT
        db.commit()
        db.refresh(purchase)

        return purchase

    except Exception as e:
        db.rollback()
        raise e