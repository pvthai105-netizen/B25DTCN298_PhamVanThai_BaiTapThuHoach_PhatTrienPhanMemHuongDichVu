from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from fastapi import HTTPException
from models.entities import News, Comment
from schemas.schemas import NewsCreate

class NewsService:
    """News Service: Quản lý bài viết xu hướng thời trang, tạp chí phong cách và mẹo phối đồ"""

    @staticmethod
    def get_all_news(
        db: Session, 
        category_tag: Optional[str] = None, 
        keyword: Optional[str] = None,
        limit: int = 20, 
        skip: int = 0
    ) -> List[News]:
        query = db.query(News).filter(News.is_published == True)
        
        if category_tag and category_tag != "all":
            query = query.filter(News.category_tag == category_tag)
        if keyword:
            pattern = f"%{keyword}%"
            query = query.filter(
                (News.title.ilike(pattern)) | (News.summary.ilike(pattern))
            )
            
        articles = query.order_by(News.id.desc()).offset(skip).limit(limit).all()
        for a in articles:
            a.comment_count = db.query(func.count(Comment.id)).filter(Comment.news_id == a.id).scalar() or 0
        return articles

    @staticmethod
    def get_news_by_id(db: Session, news_id: int) -> News:
        article = db.query(News).filter(News.id == news_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="Không tìm thấy bài viết thời trang")
        
        # Tăng lượt xem
        article.view_count += 1
        db.commit()
        db.refresh(article)
        article.comment_count = db.query(func.count(Comment.id)).filter(Comment.news_id == article.id).scalar() or 0
        return article

    @staticmethod
    def create_news(db: Session, news_in: NewsCreate) -> News:
        article = News(**news_in.dict())
        db.add(article)
        db.commit()
        db.refresh(article)
        return article

    @staticmethod
    def delete_news(db: Session, news_id: int) -> bool:
        article = db.query(News).filter(News.id == news_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="Bài viết không tồn tại")
        db.delete(article)
        db.commit()
        return True
