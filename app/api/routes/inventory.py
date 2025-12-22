from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.inventory import Inventory

router = APIRouter()

@router.get("/{product_id}")
def get_inventory(product_id: int, db: Session = Depends(get_db)):
    return db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first()
