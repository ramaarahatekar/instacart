from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from app.api.deps import get_db
from app.models.cart import Cart
from app.models.inventory import Inventory
from app.models.orders import Order
from app.models.order_items import OrderItem
from app.models.products import Product

router = APIRouter()


@router.post("/{user_id}")
def checkout(user_id: int, db: Session = Depends(get_db)):

    # 1️⃣ Fetch cart items
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    try:
        # 2️⃣ Inventory re-check
        for item in cart_items:
            inventory = db.query(Inventory).filter(
                Inventory.product_id == item.product_id
            ).first()

            if not inventory:
                raise HTTPException(
                    status_code=400,
                    detail=f"No inventory for product_id {item.product_id}"
                )

            if inventory.current_stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for product_id {item.product_id}"
                )

        # 3️⃣ Calculate total amount (SAFE for Postgres)
        total_amount = Decimal("0.00")

        for item in cart_items:
            product = db.query(Product).filter(
                Product.product_id == item.product_id
            ).first()

            if not product or product.price is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid product or price for product_id {item.product_id}"
                )

            total_amount += Decimal(product.price) * item.quantity

        # 4️⃣ Create order
        new_order = Order(
            user_id=user_id,
            order_status="PLACED",
            payment_status="PAID",
            total_amount=total_amount
        )

        db.add(new_order)
        db.flush()   # order_id generated here

        # 5️⃣ Insert order_items + deduct inventory
        for idx, item in enumerate(cart_items, start=1):

            order_item = OrderItem(
                order_id=new_order.order_id,
                product_id=item.product_id,
                add_to_cart_order=idx,
                reordered=False
            )
            db.add(order_item)

            inventory = db.query(Inventory).filter(
                Inventory.product_id == item.product_id
            ).first()
            inventory.current_stock -= item.quantity

        # 6️⃣ Clear cart
        db.query(Cart).filter(Cart.user_id == user_id).delete()

        # 7️⃣ Commit everything
        db.commit()

        return {
            "message": "Order placed successfully",
            "order_id": new_order.order_id,
            "total_amount": float(total_amount)
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Checkout failed: {str(e)}"
        )
