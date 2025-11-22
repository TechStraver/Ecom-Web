from sqlalchemy import Column, DateTime, Integer
from datetime import datetime

class BaseEntity:
    is_active = Column(Integer, default=1)  
    created_by = Column(Integer, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)
    updated_date = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
