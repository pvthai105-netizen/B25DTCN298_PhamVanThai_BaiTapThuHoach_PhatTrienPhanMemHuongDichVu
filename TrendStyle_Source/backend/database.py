import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Mặc định sử dụng SQLite để sinh viên chạy ngay không cần cài đặt MySQL Server phức tạp.
# Khi nộp bài hoặc triển khai MySQL, chỉ cần đổi cấu hình DATABASE_URL.
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./trendstyle.db"  # Để dùng MySQL: "mysql+pymysql://root:password@localhost:3306/trendstyle_db"
)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency cung cấp phiên làm việc CSDL cho mỗi Request"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
