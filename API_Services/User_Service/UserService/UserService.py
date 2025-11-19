# Services/UserService.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from Models.Models import UserRegister, UserLogin, User, UserRole
from Repository_DataAcess.UserRepository import create_user, get_user_by_identifier, user_exists
from Utils.Auth import create_access_token

def register_customer(db: Session, user_data: UserRegister):

    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if user_exists(db, user_data.email, user_data.username, user_data.phone_number):
        raise HTTPException(status_code=400, detail="User already exists")

    if user_data.captcha is not None:
        if user_data.captcha.strip() == "":
            raise HTTPException(status_code=400, detail="Captcha validation failed")

    user = User(
        username=user_data.username,
        email=user_data.email,
        phone_number=user_data.phone_number,
        password=user_data.password,  
        role=UserRole.CUSTOMER
    )

    return create_user(db, user)


def login_user(db: Session, login_data: UserLogin):
    user = get_user_by_identifier(db, login_data.identifier)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if login_data.password != user.password:  
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # FIX: Convert enum to string
    token = create_access_token({"sub": user.email, "role": user.role.value})

    # New Changess done here
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role.value   
    }