from pydantic import BaseModel
from typing import Optional
from base64 import b64encode

class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    rating: Optional[float]

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    rating: Optional[float]
    image_filename: str
    image_base64: Optional[str] = None

    class Config:
        orm_mode = True