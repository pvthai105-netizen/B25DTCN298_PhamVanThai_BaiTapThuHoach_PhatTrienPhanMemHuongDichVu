from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from fastapi import HTTPException
from models.entities import Product, Category, Brand, Review
from schemas.schemas import ProductCreate, ProductUpdate

class ProductService:
    """Product Service: Quản lý danh mục, tìm kiếm, lọc và phân loại sản phẩm thời trang"""

    @staticmethod
    def get_all_products(
        db: Session, 
        category_id: Optional[int] = None, 
        brand_id: Optional[int] = None,
        gender: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        keyword: Optional[str] = None,
        is_featured: Optional[bool] = None,
        limit: int = 50,
        skip: int = 0
    ) -> List[Product]:
        query = db.query(Product)

        if category_id:
            query = query.filter(Product.category_id == category_id)
        if brand_id:
            query = query.filter(Product.brand_id == brand_id)
        if gender and gender != "all":
            query = query.filter(Product.gender == gender)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        if keyword:
            search_pattern = f"%{keyword}%"
            query = query.filter(
                (Product.name.ilike(search_pattern)) | 
                (Product.description.ilike(search_pattern)) |
                (Product.sku.ilike(search_pattern))
            )
        if is_featured is not None:
            query = query.filter(Product.is_featured == is_featured)

        products = query.order_by(Product.id.desc()).offset(skip).limit(limit).all()

        # Tính toán điểm đánh giá trung bình cho mỗi sản phẩm
        for p in products:
            stats = db.query(func.avg(Review.rating), func.count(Review.id))\
                      .filter(Review.product_id == p.id).first()
            p.avg_rating = round(float(stats[0] or 5.0), 1)
            p.review_count = int(stats[1] or 0)

        return products

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
        
        stats = db.query(func.avg(Review.rating), func.count(Review.id))\
                  .filter(Review.product_id == product.id).first()
        product.avg_rating = round(float(stats[0] or 5.0), 1)
        product.review_count = int(stats[1] or 0)
        return product

    @staticmethod
    def create_product(db: Session, p_data: ProductCreate) -> Product:
        new_prod = Product(**p_data.dict())
        db.add(new_prod)
        db.commit()
        db.refresh(new_prod)
        return new_prod

    @staticmethod
    def update_product(db: Session, product_id: int, p_data: ProductUpdate) -> Product:
        product = ProductService.get_product_by_id(db, product_id)
        update_dict = p_data.dict(exclude_unset=True)
        for key, val in update_dict.items():
            setattr(product, key, val)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        product = ProductService.get_product_by_id(db, product_id)
        db.delete(product)
        db.commit()
        return True

    @staticmethod
    def get_categories(db: Session) -> List[Category]:
        return db.query(Category).all()

    @staticmethod
    def get_brands(db: Session) -> List[Brand]:
        return db.query(Brand).all()
