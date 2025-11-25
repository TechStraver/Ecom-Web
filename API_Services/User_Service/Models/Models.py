from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, Enum as SAEnum, ForeignKey, Float
from sqlalchemy.orm import relationship
from Db.Database import Base
from .BaseEntity import BaseEntity


# --------------------------
# ENUM FOR USER ROLE
# --------------------------
class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"


# --------------------------
# ADDRESS SCHEMA (Pydantic)
# --------------------------
class AddressBase(BaseModel):
    address_line: str
    city: str
    state: str
    pincode: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    place_id: Optional[str] = None  # Google Maps Place ID


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: int

    model_config = {"from_attributes": True}


# --------------------------
# USER BASE SCHEMA
# --------------------------
class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone_number: str
    role: UserRole


# --------------------------
# USER REGISTRATION SCHEMA
# --------------------------
class UserRegister(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=6)
    confirm_password: str
    captcha: str = Field(..., description="Captcha token (e.g., reCAPTCHA response)")

    # OTP fields
    email_otp: str = Field(..., min_length=4, max_length=8, description="OTP sent to email")
    phone_otp: str = Field(..., min_length=4, max_length=8, description="OTP sent to phone number")

    # Address field (manual + Google Maps)
    address: AddressCreate

    @field_validator("confirm_password")
    def confirm_password_match(cls, v, values):
        if "password" in values.data and v != values.data["password"]:
            raise ValueError("Passwords do not match")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "username": "john_doe",
                "email": "john@example.com",
                "phone_number": "9876543210",
                "password": "securePass123",
                "confirm_password": "securePass123",
                "captcha": "captcha-token",
                "email_otp": "123456",
                "phone_otp": "654321",
                "address": {
                    "address_line": "221B Baker Street",
                    "city": "London",
                    "state": "London",
                    "pincode": "NW16XE",
                    "latitude": 51.5237,
                    "longitude": -0.1585,
                    "place_id": "ChIJdY3j4YwEdkgR9Z0iZ0l5nAA"
                }
            }
        }
    }


# --------------------------
# LOGIN SCHEMA
# --------------------------
class UserLogin(BaseModel):
    identifier: str
    password: str
    captcha: str = Field(..., description="Captcha token for login")
    otp: Optional[str] = Field(None, description="OTP for 2FA if enabled")

    model_config = {
        "json_schema_extra": {
            "example": {
                "identifier": "john@example.com",
                "password": "securePass123",
                "captcha": "captcha-token",
                "otp": "123456"
            }
        }
    }


# --------------------------
# USER RESPONSE SCHEMA
# --------------------------
class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone_number: str
    role: UserRole
    is_active: bool
    addresses: List[AddressResponse] = []

    model_config = {"from_attributes": True}


# --------------------------
# SQLALCHEMY MODELS
# --------------------------
class User(Base, BaseEntity):
    __tablename__ = "users"
    __table_args__ = {"schema": "admin"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True)

    # Captcha fields
    captcha_token = Column(String(500), nullable=True)
    captcha_verified = Column(Boolean, default=False)

    # OTP fields
    email_otp = Column(String(10), nullable=True)
    phone_otp = Column(String(10), nullable=True)
    otp_verified = Column(Boolean, default=False)

    # Relationship
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")


class Address(Base, BaseEntity):
    __tablename__ = "addresses"
    __table_args__ = {"schema": "admin"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("admin.users.id"), nullable=False)

    address_line = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=False)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    place_id = Column(String(200), nullable=True)  # Google Maps Place ID

    # Relationship
    user = relationship("User", back_populates="addresses")
