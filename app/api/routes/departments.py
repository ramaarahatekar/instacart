from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.departments import Department

router = APIRouter()

@router.get("/")
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()
