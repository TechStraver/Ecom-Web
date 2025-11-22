from http.client import HTTPException
from Repository_DataAcess.ProductRepo import get_product_by_id, update_product
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from Db.Database import SessionLocal
import base64

from ProductService.ProductService import (
    add_product,
    fetch_all_products,
    update_product_details
)
from Schema.product_schema import ProductUpdate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/product/save")
def save_product(
    product_id: int = Form(0),
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    current_user_id: int = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # -------- INSERT --------
    if product_id == 0 or product_id is None:
        if not image:
            raise HTTPException(status_code=400, detail="Image is required for new product")

        new_product = add_product(
            db=db,
            name=name,
            description=description,
            price=price,
            current_user_id=current_user_id,
            image=image
        )
        return {
            "message": "Product created successfully",
            "product_id": new_product.id
        }

    # -------- UPDATE --------
    update_data = {
        "name": name,
        "description": description,
        "price": price
    }

    return update_product_details(
        db=db,
        product_id=product_id,
        update_data=update_data,
        current_user_id=current_user_id,
        image=image
    )


@router.get("/product/all")
def get_all_products(db: Session = Depends(get_db)):
    products = fetch_all_products(db)
    result = []

    for p in products:
        image_base64 = base64.b64encode(p.image_blob).decode() if p.image_blob else None

        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "is_active": p.is_active,
            "rating": p.rating,
            "image_filename": p.image_filename,
            "image_base64": image_base64
        })

    return result


@router.delete("/product/delete/{product_id}")
def delete_product_soft(
    product_id: int,
    current_user_id: int,
    db: Session = Depends(get_db)
):
    from datetime import datetime
    product = get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = {
        "is_active": 0,
        "updated_by": current_user_id,
        "updated_date": datetime.utcnow()
    }

    updated = update_product(db, product_id, update_data)

    return {
        "message": "Product deleted successfully (soft delete)",
        "product_id": product_id
    }