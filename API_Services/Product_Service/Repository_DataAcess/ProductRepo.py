from sqlalchemy.orm import Session
# from sqlalchemy import asc, desc
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

def get_all_products(
    db: Session,
    search: str | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    page: int = 1,
    page_size: int = 10
):
    query = db.query(Product)

    # --- Search filter ---
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Product.name.ilike(search_term)) |
            (Product.description.ilike(search_term))
        )

    # --- Sorting ---
    sort_column = getattr(Product, sort_by, Product.id)
    if sort_order.lower() == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    # --- Pagination ---
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return items, total
