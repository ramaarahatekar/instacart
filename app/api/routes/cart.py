from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.cart import Cart
from app.models.inventory import Inventory

router = APIRouter()
@router.post("/add")
def add_to_cart(
    user_id: int,
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first()

    if not inventory or inventory.current_stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    cart_item = Cart(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )

    db.add(cart_item)
    db.commit()
    return {"message": "Item added to cart"}
@router.get("/{user_id}")
def view_cart(user_id: int, db: Session = Depends(get_db)):
    return db.query(Cart).filter(Cart.user_id == user_id).all()

@router.delete("/remove")
def remove_from_cart(cart_id: int, db: Session = Depends(get_db)):
    item = db.query(Cart).filter(Cart.cart_id == cart_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}
