# models/user_model.py
from enum import Enum

class UserRole(str, Enum):
    CUSTOMER = "customer"
    DELIVERY_BOY = "delivery_boy"
    SELLER = "seller"
    ADMIN = "admin"
