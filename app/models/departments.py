from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True)
    department = Column(String(100))
