from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.products import Product

router = APIRouter()

@router.get("/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.is_active == True).all()

@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.product_id == product_id).first()
