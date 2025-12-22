from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from app.core.database import Base

class InventoryAlert(Base):
    __tablename__ = "inventory_alerts"

    alert_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    alert_type = Column(String(50))
    message = Column(Text)
    created_at = Column(TIMESTAMP)
