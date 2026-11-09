from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.entities import Review, Product, User
from schemas.schemas import ReviewCreate

class ReviewService:
    """Review Service: Quản lý đánh giá số sao (1-5 sao) và nhận xét chất lượng sản phẩm"""

    @staticmethod
    def get_product_reviews(db: Session, product_id: int):
        reviews = db.query(Review).filter(Review.product_id == product_id).order_by(Review.id.desc()).all()
        result = []
        for r in reviews:
            result.append({
                "id": r.id,
                "product_id": r.product_id,
                "user_id": r.user_id,
                "user_name": r.user.full_name if r.user else "Khách hàng",
                "rating": r.rating,
                "title": r.title,
                "comment": r.comment,
                "created_at": r.created_at
            })
        return result

    @staticmethod
    def create_review(db: Session, user_id: int, r_in: ReviewCreate):
        # Kiểm tra sản phẩm tồn tại
        prod = db.query(Product).filter(Product.id == r_in.product_id).first()
        if not prod:
            raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")

        # Kiểm tra người dùng đã đánh giá chưa (mỗi người 1 đánh giá chính thức)
        existing = db.query(Review).filter(
            Review.product_id == r_in.product_id,
            Review.user_id == user_id
        ).first()

        if existing:
            existing.rating = r_in.rating
            existing.title = r_in.title
            existing.comment = r_in.comment
            db.commit()
            db.refresh(existing)
            review = existing
        else:
            review = Review(
                product_id=r_in.product_id,
                user_id=user_id,
                rating=r_in.rating,
                title=r_in.title,
                comment=r_in.comment
            )
            db.add(review)
            db.commit()
            db.refresh(review)

        return {
            "id": review.id,
            "product_id": review.product_id,
            "user_id": review.user_id,
            "user_name": review.user.full_name if review.user else "Khách hàng",
            "rating": review.rating,
            "title": review.title,
            "comment": review.comment,
            "created_at": review.created_at
        }

    @staticmethod
    def delete_review(db: Session, user_id: int, review_id: int, is_admin: bool = False):
        query = db.query(Review).filter(Review.id == review_id)
        if not is_admin:
            query = query.filter(Review.user_id == user_id)
        
        review = query.first()
        if not review:
            raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá hoặc không có quyền xóa")
        
        db.delete(review)
        db.commit()
        return True
