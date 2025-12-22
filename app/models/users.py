from sqlalchemy import Column, Integer, String, TIMESTAMP
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    created_at = Column(
        TIMESTAMP,
        default=datetime.utcnow
    )
