# Services/ProductService.py

import os
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile

from Model.ProductModel import Product
from Repository_DataAcess.ProductRepo import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product
)

PRODUCT_IMAGE_DIR = "Product_Catalog"


def ensure_image_folder_exists():
    if not os.path.exists(PRODUCT_IMAGE_DIR):
        os.makedirs(PRODUCT_IMAGE_DIR)


def save_product_image(image: UploadFile, product_id: int) -> str:
    ensure_image_folder_exists()

    file_extension = image.filename.split(".")[-1]
    filename = f"{product_id}_{datetime.utcnow().timestamp()}.{file_extension}"

    filepath = os.path.join(PRODUCT_IMAGE_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(image.file.read())

    return filename

def add_product(db, name, description, price, current_user_id, image):

    # Read image bytes
    image_data = image.file.read()
    filename = image.filename

    # Save image in Product_Catalog
    folder = "Product_Catalog"
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, filename)
    with open(path, "wb") as f:
        f.write(image_data)

    product = Product(
        name=name,
        description=description,
        price=price,
        image_filename=filename,
        image_blob=image_data,
        created_by=current_user_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product



def fetch_all_products(db: Session):
    products = get_all_products(db)
    return products


def update_product_details(db: Session, product_id: int, update_data, current_user_id: int, image: UploadFile | None):

    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data["updated_by"] = current_user_id
    update_data["updated_date"] = datetime.utcnow()

    updated = update_product(db, product_id, update_data)


    if image:
        saved_filename = save_product_image(image, product_id)
        update_product(db, product_id, {"image": saved_filename})

    return {
        "message": "Product updated successfully",
        "product_id": product_id
    }