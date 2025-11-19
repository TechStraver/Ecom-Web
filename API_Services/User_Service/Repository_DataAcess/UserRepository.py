# Db/UserRepository.py
from sqlalchemy.orm import Session
from Models.Models import User

def get_user_by_identifier(db: Session, identifier: str) -> User | None:
    """
    Find a user by email, username, or phone number.
    """
    return db.query(User).filter(
        (User.email == identifier) |
        (User.username == identifier) |
        (User.phone_number == identifier)
    ).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Find a user by email only.
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Find a user by username only.
    """
    return db.query(User).filter(User.username == username).first()

def get_user_by_phone(db: Session, phone_number: str) -> User | None:
    """
    Find a user by phone number only.
    """
    return db.query(User).filter(User.phone_number == phone_number).first()

def create_user(db: Session, user: User) -> User:
    """
    Insert a new user into the database.
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def user_exists(db: Session, email: str, username: str, phone_number: str) -> bool:
    """
    Check if a user already exists by email, username, or phone number.
    """
    return db.query(User).filter(
        (User.email == email) |
        (User.username == username) |
        (User.phone_number == phone_number)
    ).first() is not None
