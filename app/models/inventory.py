from sqlalchemy import Column, Integer, TIMESTAMP
from app.core.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    product_id = Column(Integer, primary_key=True, index=True)
    current_stock = Column(Integer)
    reorder_level = Column(Integer)
    last_updated = Column(TIMESTAMP)
