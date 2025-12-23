from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP
from app.core.database import Base
from datetime import datetime

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)

    order_status = Column(String(20))
    payment_status = Column(String(20))

    total_amount = Column(Numeric(10, 2))
    order_timestamp = Column(TIMESTAMP, default=datetime.utcnow)
