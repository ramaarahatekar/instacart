from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.aisles import Aisle

router = APIRouter()

@router.get("/")
def get_aisles(db: Session = Depends(get_db)):
    return db.query(Aisle).all()
