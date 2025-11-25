from typing import Optional, List
from sqlalchemy.orm import Session
from Models.Models import Address, User


# -------------------------------------------------------
# CREATE ADDRESS
# -------------------------------------------------------
def create_address(db: Session, user: User, address: Address) -> Address:
    """
    Add a new address for a given user.
    """
    address.user = user
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


# -------------------------------------------------------
# READ ADDRESSES
# -------------------------------------------------------
def get_address_by_id(db: Session, address_id: int) -> Optional[Address]:
    return db.query(Address).filter(Address.id == address_id).first()


def get_addresses_by_user(db: Session, user_id: int) -> List[Address]:
    return db.query(Address).filter(Address.user_id == user_id).all()


# -------------------------------------------------------
# UPDATE ADDRESS
# -------------------------------------------------------
def update_address(db: Session, address_id: int, updated_data: dict) -> Optional[Address]:
    address = get_address_by_id(db, address_id)
    if not address:
        return None

    for key, value in updated_data.items():
        if hasattr(address, key):
            setattr(address, key, value)

    db.commit()
    db.refresh(address)
    return address


# -------------------------------------------------------
# DELETE ADDRESS
# -------------------------------------------------------
def delete_address(db: Session, address_id: int) -> bool:
    address = get_address_by_id(db, address_id)
    if not address:
        return False

    db.delete(address)
    db.commit()
    return True
