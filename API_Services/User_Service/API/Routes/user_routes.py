# Api/Routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Db.Database import SessionLocal
from Models.Models import UserRegister, UserLogin, UserResponse
from UserService.UserService import register_customer, login_user

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Registration endpoint (Customer only)
@router.post("/register", response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    return register_customer(db, user)

# Login endpoint (any role)
@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, login_data)
