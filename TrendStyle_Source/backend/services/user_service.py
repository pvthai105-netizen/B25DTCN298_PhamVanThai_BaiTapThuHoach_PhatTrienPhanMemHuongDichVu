from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.entities import User
from schemas.schemas import UserUpdate, ChangePassword
from services.auth_service import AuthService

class UserService:
    """User Service: Quản lý hồ sơ, cập nhật thông tin và mật khẩu người dùng"""

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
        return user

    @staticmethod
    def update_profile(db: Session, user_id: int, update_data: UserUpdate) -> User:
        user = UserService.get_user_by_id(db, user_id)
        if update_data.full_name is not None:
            user.full_name = update_data.full_name
        if update_data.phone is not None:
            user.phone = update_data.phone
        if update_data.address is not None:
            user.address = update_data.address
        
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def change_password(db: Session, user_id: int, pass_data: ChangePassword) -> bool:
        user = UserService.get_user_by_id(db, user_id)
        if not AuthService.verify_password(pass_data.old_password, user.password_hash):
            raise HTTPException(status_code=400, detail="Mật khẩu cũ không chính xác")
        
        user.password_hash = AuthService.hash_password(pass_data.new_password)
        db.commit()
        return True
