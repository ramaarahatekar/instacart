from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Aisle(Base):
    __tablename__ = "aisles"

    aisle_id = Column(Integer, primary_key=True, index=True)
    aisle = Column(String(100))
