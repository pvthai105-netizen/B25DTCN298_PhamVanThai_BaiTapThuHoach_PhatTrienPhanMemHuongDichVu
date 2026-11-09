from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.entities import Comment, News, User
from schemas.schemas import CommentCreate

class CommentService:
    """Comment Service: Quản lý thảo luận, ý kiến đóng góp của độc giả dưới bài viết xu hướng"""

    @staticmethod
    def get_news_comments(db: Session, news_id: int):
        comments = db.query(Comment).filter(Comment.news_id == news_id).order_by(Comment.id.desc()).all()
        result = []
        for c in comments:
            result.append({
                "id": c.id,
                "news_id": c.news_id,
                "user_id": c.user_id,
                "user_name": c.user.full_name if c.user else "Độc giả",
                "content": c.content,
                "created_at": c.created_at
            })
        return result

    @staticmethod
    def create_comment(db: Session, user_id: int, c_in: CommentCreate):
        news = db.query(News).filter(News.id == c_in.news_id).first()
        if not news:
            raise HTTPException(status_code=404, detail="Bài viết không tồn tại")

        comment = Comment(
            news_id=c_in.news_id,
            user_id=user_id,
            content=c_in.content
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)

        return {
            "id": comment.id,
            "news_id": comment.news_id,
            "user_id": comment.user_id,
            "user_name": comment.user.full_name if comment.user else "Độc giả",
            "content": comment.content,
            "created_at": comment.created_at
        }

    @staticmethod
    def delete_comment(db: Session, user_id: int, comment_id: int, is_admin: bool = False):
        query = db.query(Comment).filter(Comment.id == comment_id)
        if not is_admin:
            query = query.filter(Comment.user_id == user_id)
        
        c = query.first()
        if not c:
            raise HTTPException(status_code=404, detail="Bình luận không tồn tại hoặc không có quyền xóa")
        
        db.delete(c)
        db.commit()
        return True
