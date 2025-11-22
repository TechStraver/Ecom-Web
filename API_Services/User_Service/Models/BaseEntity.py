from sqlalchemy import Column, Boolean, DateTime, Integer, ForeignKey
from datetime import datetime

class BaseEntity:
    is_active = Column(Integer, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_date = Column(DateTime, default=None, onupdate=datetime.utcnow)