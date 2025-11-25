from sqlalchemy.orm import Session
from Model.ProductModel import Product

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_name(db: Session, name: str) -> Product | None:
    return db.query(Product).filter(Product.name == name).first()

def create_product(db: Session, product: Product) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db: Session, product_id: int, update_data: dict) -> Product | None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

def soft_delete_product(db: Session, product_id: int, update_data: dict) -> Product | None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product
