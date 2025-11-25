from sqlalchemy import Column, Boolean, DateTime, Integer, ForeignKey
from datetime import datetime

class BaseEntity:
    # Active flag (Boolean instead of Integer for clarity)
    is_active = Column(Boolean, default=True, nullable=False)

    # Audit fields
    created_by = Column(Integer, ForeignKey("admin.users.id"), nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    updated_by = Column(Integer, ForeignKey("admin.users.id"), nullable=True)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
