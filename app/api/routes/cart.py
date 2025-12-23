from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.cart import Cart
from app.models.inventory import Inventory
from app.models.products import Product
from app.models.departments import Department


router = APIRouter()
@router.post("/add")
def add_to_cart(
    user_id: int,
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first()

    if not inventory or inventory.current_stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    existing_item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == product_id
    ).first()

    if existing_item:
        existing_item.quantity += quantity
    else:
        db.add(Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        ))

    db.commit()
    return {"message": "Item added to cart"}




@router.get("/{user_id}")
def view_cart(user_id: int, db: Session = Depends(get_db)):

    cart_items = (
        db.query(
            Cart.cart_id,
            Cart.product_id,
            Cart.quantity,
            Cart.added_at,
            Product.product_name,
            Product.price,
            Department.department_name
        )
        .join(Product, Cart.product_id == Product.product_id)
        .join(Department, Product.department_id == Department.department_id)
        .filter(Cart.user_id == user_id)
        .all()
    )

    response = []
    for item in cart_items:
        response.append({
            "cart_id": item.cart_id,
            "product_id": item.product_id,
            "product_name": item.product_name,
            "department": item.department,
            "price": round(float(item.price), 2)
,
            "quantity": item.quantity,
            "subtotal": round(float(item.price) * item.quantity, 2)
,
            "added_at": item.added_at
        })

    return response

@router.patch("/update")
def update_cart_quantity(
    user_id: int,
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be >= 1")

    cart_item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first()

    if not inventory or inventory.current_stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    cart_item.quantity = quantity
    db.commit()

    return {
        "message": "Cart updated successfully",
        "user_id": user_id,
        "product_id": product_id,
        "quantity": quantity
    }

@router.delete("/clear/{user_id}")
def clear_cart(user_id: int, db: Session = Depends(get_db)):

    deleted = db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()

    return {
        "message": "Cart cleared successfully",
        "items_removed": deleted
    }




@router.delete("/remove")
def remove_from_cart(cart_id: int, db: Session = Depends(get_db)):
    item = db.query(Cart).filter(Cart.cart_id == cart_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}
