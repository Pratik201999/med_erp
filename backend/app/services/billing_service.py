from sqlalchemy.orm import Session
from app.models.bill import Bill
from app.models.bill_item import BillItem
from app.services.inventory_service import stock_out

def create_bill(db: Session, shop_id, items, discount=0, payment_mode="CASH"):
    try:
        bill = Bill(
            shop_id=shop_id,
            total_amount=0,
            discount=discount,
            gst_amount=0,
            payment_mode=payment_mode
        )
        db.add(bill)
        db.commit()
        db.refresh(bill)

        total = 0

        for item in items:
            if item["quantity"] <= 0:
                raise Exception("Invalid quantity")

            # Deduct stock
            stock_out(db, item["batch_id"], item["quantity"], "BILL", bill.id)

            line_total = item["quantity"] * item["price"]

            bill_item = BillItem(
                bill_id=bill.id,
                batch_id=item["batch_id"],
                quantity=item["quantity"],
                price=item["price"],
                gst=0  # optional per-item GST later
            )

            db.add(bill_item)

            total += line_total

        # Apply discount
        discounted_total = total - discount

        # GST after discount
        gst_total = discounted_total * 0.12

        final_total = discounted_total + gst_total

        bill.gst_amount = gst_total
        bill.total_amount = final_total

        db.commit()

        return bill

    except Exception as e:
        db.rollback()
        raise e