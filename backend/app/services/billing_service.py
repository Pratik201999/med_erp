from sqlalchemy.orm import Session
from app.models.bill import Bill
from app.models.bill_item import BillItem
from app.models.batch import Batch
from app.services.inventory_service import stock_out
from datetime import date


def create_bill(db: Session, shop_id, items, discount=0, payment_mode="CASH"):
    try:
        total = 0

        # 🧾 Create bill (NO COMMIT)
        bill = Bill(
            shop_id=shop_id,
            total_amount=0,
            discount=discount,
            gst_amount=0,
            payment_mode=payment_mode
        )

        db.add(bill)
        db.flush()  # get bill.id

        for item in items:

            if item["quantity"] <= 0:
                raise Exception("Invalid quantity")

            remaining_qty = item["quantity"]

            # 🔥 Fetch batches (latest expiry first, skip expired)
            batches = db.query(Batch).filter(
                Batch.medicine_id == item["medicine_id"],
                Batch.shop_id == shop_id,
                Batch.quantity > 0,
                Batch.expiry_date >= date.today()  # skip expired stock
            ).order_by(
                Batch.expiry_date.asc()  # 🔥 latest expiry first
            ).all()

            if not batches:
                raise Exception(f"No stock available for medicine {item['medicine_id']}")

            for batch in batches:

                if remaining_qty <= 0:
                    break

                available = batch.quantity
                consume = min(available, remaining_qty)

                # 📉 Deduct stock
                stock_out(db, batch.id, consume, "BILL", bill.id)

                # 🧾 Create bill item (per batch)
                bill_item = BillItem(
                    bill_id=bill.id,
                    batch_id=batch.id,
                    quantity=consume,
                    price=item["price"],
                    gst=0
                )

                db.add(bill_item)

                total += consume * item["price"]
                remaining_qty -= consume

            # ❌ Not enough stock overall
            if remaining_qty > 0:
                raise Exception("Insufficient total stock")

        # 💸 Apply discount
        discounted_total = total - discount

        if discounted_total < 0:
            raise Exception("Discount cannot exceed total amount")

        # 🧮 GST (12%)
        gst_total = discounted_total * 0.12
        final_total = discounted_total + gst_total

        bill.gst_amount = gst_total
        bill.total_amount = final_total

        # ✅ SINGLE COMMIT
        db.commit()
        db.refresh(bill)

        return bill

    except Exception as e:
        db.rollback()
        raise e