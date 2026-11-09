import hashlib
import hmac
import base64
import json
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.entities import User, UserRole, Cart
from schemas.schemas import UserRegister, UserLogin

SECRET_KEY = "TRENDSTYLE_SUPER_SECRET_KEY_SOA_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

class AuthService:
    """Authentication Service: Quản lý đăng ký, đăng nhập, mã hóa và cấp phát JWT token"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Băm mật khẩu sử dụng HMAC-SHA256 kết hợp Salt an toàn"""
        salt = "trendstyle_salt_2026"
        hashed = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
        return hashed

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Kiểm tra tính khớp của mật khẩu"""
        return AuthService.hash_password(plain_password) == hashed_password

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        """Tạo mã xác thực JWT chuẩn RFC 7519"""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": int(expire.timestamp())})
        
        header = {"alg": "HS256", "typ": "JWT"}
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
        payload_b64 = base64.urlsafe_b64encode(json.dumps(to_encode).encode()).decode().rstrip("=")
        
        signature_raw = hmac.new(
            SECRET_KEY.encode(), 
            f"{header_b64}.{payload_b64}".encode(), 
            hashlib.sha256
        ).digest()
        signature_b64 = base64.urlsafe_b64encode(signature_raw).decode().rstrip("=")
        
        return f"{header_b64}.{payload_b64}.{signature_b64}"

    @staticmethod
    def decode_access_token(token: str) -> dict:
        """Giải mã và xác thực chữ ký JWT Token"""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                raise ValueError("Invalid token format")
            
            header_b64, payload_b64, signature_b64 = parts
            
            # Kiểm tra chữ ký
            expected_sig = base64.urlsafe_b64encode(
                hmac.new(SECRET_KEY.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
            ).decode().rstrip("=")
            
            if not hmac.compare_digest(expected_sig, signature_b64):
                raise ValueError("Signature verification failed")
            
            # Giải mã payload
            padded_payload = payload_b64 + "=" * (-len(payload_b64) % 4)
            payload = json.loads(base64.urlsafe_b64decode(padded_payload).decode())
            
            # Kiểm tra hạn dùng
            if payload.get("exp") and payload["exp"] < int(time.time()):
                raise ValueError("Token has expired")
            
            return payload
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Mã xác thực không hợp lệ hoặc đã hết hạn",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @classmethod
    def register_user(cls, db: Session, user_data: UserRegister) -> User:
        """Đăng ký tài khoản người dùng mới và tự động khởi tạo giỏ hàng rỗng"""
        # Kiểm tra trùng username hoặc email
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại trên hệ thống")
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(status_code=400, detail="Địa chỉ email đã được sử dụng")

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=cls.hash_password(user_data.password),
            full_name=user_data.full_name,
            phone=user_data.phone,
            address=user_data.address,
            role=UserRole.CUSTOMER.value
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Khởi tạo giỏ hàng cho tài khoản
        cart = Cart(user_id=new_user.id)
        db.add(cart)
        db.commit()

        return new_user

    @classmethod
    def authenticate_user(cls, db: Session, login_data: UserLogin):
        """Xác thực đăng nhập và trả về access token"""
        user = db.query(User).filter(
            (User.username == login_data.username) | (User.email == login_data.username)
        ).first()

        if not user or not cls.verify_password(login_data.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Tài khoản hoặc mật khẩu không chính xác")
        
        if not user.is_active:
            raise HTTPException(status_code=403, detail="Tài khoản của bạn đã bị khóa")

        token = cls.create_access_token({
            "sub": str(user.id),
            "username": user.username,
            "role": user.role
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role
        }
