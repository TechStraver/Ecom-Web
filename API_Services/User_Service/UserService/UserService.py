from sqlalchemy.orm import Session
from fastapi import HTTPException  # type: ignore
from Models.Models import UserRegister, UserLogin, User, UserRole
from Repository_DataAcess.UserRepository import (
    create_user,
    get_user_by_identifier,
    user_exists,
)
from Repository_DataAcess.AddressRepository import (
    create_address,
    get_addresses_by_user,
    get_address_by_id,
    update_address,
    delete_address,
)
from Utils.Auth import (
    create_access_token,
    verify_captcha,
    verify_otp,
    hash_password,
    verify_password,
)


# -------------------------------------------------------
# REGISTER CUSTOMER (address = null at registration)
# -------------------------------------------------------
def register_customer(db: Session, user_data: UserRegister):
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if user_exists(db, user_data.email, user_data.username, user_data.phone_number):
        raise HTTPException(status_code=400, detail="User already exists")

    if not user_data.captcha or not verify_captcha(user_data.captcha):
        raise HTTPException(status_code=400, detail="Captcha validation failed")

    if not verify_otp(user_data.email_otp, user_data.email_otp) or not verify_otp(
        user_data.phone_otp, user_data.phone_otp
    ):
        raise HTTPException(status_code=400, detail="OTP validation failed")

    user = User(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        phone_number=user_data.phone_number,
        password=hash_password(user_data.password),
        role=UserRole.CUSTOMER,
        captcha_token=user_data.captcha,
        captcha_verified=True,
        email_otp=user_data.email_otp,
        phone_otp=user_data.phone_otp,
        otp_verified=True,
    )

    # At registration → no addresses
    return create_user(db, user, addresses=None)


# -------------------------------------------------------
# LOGIN USER
# -------------------------------------------------------
def login_user(db: Session, login_data: UserLogin):
    user = get_user_by_identifier(db, login_data.identifier)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not login_data.captcha or not verify_captcha(login_data.captcha):
        raise HTTPException(status_code=400, detail="Captcha validation failed")

    if login_data.otp and not verify_otp(login_data.otp, user.phone_otp):
        raise HTTPException(status_code=400, detail="OTP validation failed")

    token = create_access_token({"sub": user.email, "role": user.role.value})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role.value,
    }


# -------------------------------------------------------
# ADDRESS CRUD OPERATIONS
# -------------------------------------------------------
def add_address(db: Session, user_id: int, address_data):
    user = get_user_by_identifier(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return create_address(db, user, address_data)


def get_user_addresses(db: Session, user_id: int):
    return get_addresses_by_user(db, user_id)


def get_single_address(db: Session, address_id: int):
    address = get_address_by_id(db, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


def edit_address(db: Session, address_id: int, updated_data: dict):
    address = update_address(db, address_id, updated_data)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


def remove_address(db: Session, address_id: int):
    success = delete_address(db, address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"detail": "Address deleted successfully"}
