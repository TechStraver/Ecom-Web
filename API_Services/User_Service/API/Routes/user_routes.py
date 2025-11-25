from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Db.Database import SessionLocal
from Models.Models import UserRegister, UserLogin, UserResponse, AddressCreate, AddressResponse
from UserService.UserService import (
    register_customer,
    login_user,
    add_address,
    get_user_addresses,
    get_single_address,
    edit_address,
    remove_address,
)

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------------
# Registration endpoint (Customer only)
# -------------------------------------------------------
@router.post("/register", response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    return register_customer(db, user)


# -------------------------------------------------------
# Login endpoint (any role)
# -------------------------------------------------------
@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, login_data)


# -------------------------------------------------------
# ADDRESS CRUD ENDPOINTS
# -------------------------------------------------------

# Add new address for a user
@router.post("/users/{user_id}/addresses", response_model=AddressResponse)
def create_address(user_id: int, address: AddressCreate, db: Session = Depends(get_db)):
    return add_address(db, user_id, address)


# Get all addresses for a user
@router.get("/users/{user_id}/addresses", response_model=list[AddressResponse])
def list_addresses(user_id: int, db: Session = Depends(get_db)):
    return get_user_addresses(db, user_id)


# Get single address by ID
@router.get("/addresses/{address_id}", response_model=AddressResponse)
def read_address(address_id: int, db: Session = Depends(get_db)):
    return get_single_address(db, address_id)


# Update address by ID
@router.put("/addresses/{address_id}", response_model=AddressResponse)
def update_address(address_id: int, updated_data: dict, db: Session = Depends(get_db)):
    return edit_address(db, address_id, updated_data)


# Delete address by ID
@router.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    return remove_address(db, address_id)
