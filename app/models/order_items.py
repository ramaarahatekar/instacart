from sqlalchemy import Column, Integer, Boolean
from app.core.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer)
    product_id = Column(Integer)
    add_to_cart_order = Column(Integer)
    reordered = Column(Boolean, default=False)
