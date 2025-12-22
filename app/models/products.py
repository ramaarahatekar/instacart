from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text, TIMESTAMP
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(Text)
    aisle_id = Column(Integer)
    department_id = Column(Integer)
    price = Column(Numeric(10, 2))
    brand = Column(String(100))
    unit = Column(String(20))
    is_active = Column(Boolean)
    created_at = Column(TIMESTAMP)
