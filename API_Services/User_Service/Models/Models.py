from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum as PyEnum
from Db.Database import Base
from .BaseEntity import BaseEntity
from sqlalchemy import Column, Integer, String, Enum, Boolean
# Base schema
class UserRole(PyEnum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    role: UserRole

# Registration schema (only for Customer)
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone_number: str
    password: str = Field(..., min_length=6)
    confirm_password: str
    captcha: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "phone_number": "9876543210",
                "password": "securePass123",
                "confirm_password": "securePass123",
                "captcha": "captcha-token"
            }
        }

# Login schema (any role, flexible identifier)
class UserLogin(BaseModel):
    identifier: str  # can be email OR username OR phone_number
    password: str

    class Config:
        schema_extra = {
            "example": {
                "identifier": "john@example.com",
                "password": "securePass123"
            }
        }

# Response schema
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str
    role: str
    is_active: bool

    class Config:
        orm_mode = True

class User(Base,BaseEntity):
    __tablename__ = "users"
    __table_args__ = {"schema": "admin"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)