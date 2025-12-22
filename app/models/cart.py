from sqlalchemy import Column, Integer, TIMESTAMP
from datetime import datetime
from app.core.database import Base

class Cart(Base):
    __tablename__ = "cart"

    cart_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    added_at = Column(
        TIMESTAMP,
        default=datetime.utcnow
    )
