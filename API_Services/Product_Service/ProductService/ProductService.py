import os
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile

from Model.ProductModel import Product
from Repository_DataAcess.ProductRepo import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    soft_delete_product
)

PRODUCT_IMAGE_DIR = "Product_Catalog"

def ensure_image_folder_exists():
    if not os.path.exists(PRODUCT_IMAGE_DIR):
        os.makedirs(PRODUCT_IMAGE_DIR)

def save_product_image(image: UploadFile, product_id: int) -> tuple[str, bytes]:
    ensure_image_folder_exists()
    file_extension = image.filename.split(".")[-1]
    filename = f"{product_id}_{datetime.utcnow().timestamp()}.{file_extension}"
    filepath = os.path.join(PRODUCT_IMAGE_DIR, filename)

    image_data = image.file.read()
    with open(filepath, "wb") as buffer:
        buffer.write(image_data)

    return filename, image_data

def add_product(db: Session, name: str, description: str, price: float, current_user_id: int, image: UploadFile):
    if not image:
        raise HTTPException(status_code=400, detail="Image is required for new product")

    image_data = image.file.read()
    filename = image.filename

    # Save image file
    ensure_image_folder_exists()
    path = os.path.join(PRODUCT_IMAGE_DIR, filename)
    with open(path, "wb") as f:
        f.write(image_data)

    product = Product(
        name=name,
        description=description,
        price=price,
        image_filename=filename,
        image_blob=image_data,
        created_by=current_user_id,
        created_date=datetime.utcnow(),
        is_active=1
    )

    return create_product(db, product)

def fetch_all_products(db: Session):
    return get_all_products(db)

def update_product_details(db: Session, product_id: int, update_data: dict, current_user_id: int, image: UploadFile | None):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data["updated_by"] = current_user_id
    update_data["updated_date"] = datetime.utcnow()

    updated = update_product(db, product_id, update_data)

    if image:
        filename, image_data = save_product_image(image, product_id)
        update_product(db, product_id, {"image_filename": filename, "image_blob": image_data})

    return {
        "message": "Product updated successfully",
        "product_id": product_id
    }

def soft_delete_product_service(db: Session, product_id: int, current_user_id: int):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = {
        "is_active": 0,
        "updated_by": current_user_id,
        "updated_date": datetime.utcnow()
    }

    soft_delete_product(db, product_id, update_data)

    return {
        "message": "Product deleted successfully (soft delete)",
        "product_id": product_id
    }
