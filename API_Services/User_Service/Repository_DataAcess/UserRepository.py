from typing import Optional, List
from sqlalchemy.orm import Session
from Models.Models import User, Address


# -------------------------------------------------------
# FETCH USER BY EMAIL | USERNAME | PHONE (Generic Lookup)
# -------------------------------------------------------
def get_user_by_identifier(db: Session, identifier: str) -> Optional[User]:
    """
    Find user using email OR username OR phone number.
    """
    return (
        db.query(User)
        .filter(
            (User.email == identifier)
            | (User.username == identifier)
            | (User.phone_number == identifier)
        )
        .first()
    )


# -------------------------------------------------------
# INDIVIDUAL LOOKUPS
# -------------------------------------------------------
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_phone(db: Session, phone_number: str) -> Optional[User]:
    return db.query(User).filter(User.phone_number == phone_number).first()


# -------------------------------------------------------
# CREATE USER (with optional addresses)
# -------------------------------------------------------
def create_user(db: Session, user: User, addresses: Optional[List[Address]] = None) -> User:
    """
    Save a new user to the database, with optional addresses.
    """
    db.add(user)
    if addresses:
        for addr in addresses:
            addr.user = user
            db.add(addr)
    db.commit()
    db.refresh(user)
    return user


# -------------------------------------------------------
# CHECK USER EXISTS (EMAIL | USERNAME | PHONE)
# -------------------------------------------------------
def user_exists(db: Session, email: str, username: str, phone_number: str) -> bool:
    """
    Check if a user already exists by email, username, or phone.
    """
    return (
        db.query(User)
        .filter(
            (User.email == email)
            | (User.username == username)
            | (User.phone_number == phone_number)
        )
        .first()
        is not None
    )


# -------------------------------------------------------
# UPDATE CAPTCHA STATUS
# -------------------------------------------------------
def update_captcha_status(db: Session, user: User, verified: bool) -> User:
    """
    Update captcha verification status for a user.
    """
    user.captcha_verified = verified
    db.commit()
    db.refresh(user)
    return user


# -------------------------------------------------------
# UPDATE OTP STATUS
# -------------------------------------------------------
def update_otp_status(db: Session, user: User, email_verified: bool = False, phone_verified: bool = False) -> User:
    """
    Update OTP verification flags for a user.
    """
    if email_verified and phone_verified:
        user.otp_verified = True
    db.commit()
    db.refresh(user)
    return user


# -------------------------------------------------------
# ADD ADDRESS TO USER
# -------------------------------------------------------

