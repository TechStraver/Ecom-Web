import datetime
from .BaseEntity import BaseEntity
from Db.Database import Base
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, LargeBinary
from sqlalchemy.sql import func

class Product(Base,BaseEntity):
    __tablename__ = "products"
    __table_args__ = {"schema": "admin"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, default=0.0, nullable=True)
    image_blob = Column(LargeBinary, nullable=False)
    image_filename = Column(String, nullable=False)
