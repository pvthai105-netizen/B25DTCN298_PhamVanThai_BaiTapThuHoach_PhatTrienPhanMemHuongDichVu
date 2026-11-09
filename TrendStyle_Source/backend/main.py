import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import (
    auth_router, user_router, product_router, cart_router,
    order_router, payment_router, review_router, news_router,
    comment_router, admin_router
)
from seed_data import init_db_and_seed

app = FastAPI(
    title="TrendStyle SOA Web Services API",
    description="Hệ thống Backend hướng dịch vụ (Service-Oriented Architecture) phục vụ nền tảng TrendStyle",
    version="1.0.0"
)

# Cấu hình CORS để Frontend gọi API dễ dàng
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tự động nạp CSDL và dữ liệu mẫu khi khởi động ứng dụng
@app.on_event("startup")
def on_startup():
    init_db_and_seed()

# Đăng ký 10 Router dịch vụ SOA
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(review_router)
app.include_router(news_router)
app.include_router(comment_router)
app.include_router(admin_router)

# Mount thư mục Frontend để có thể truy cập website trực tiếp từ FastAPI
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/client", StaticFiles(directory=frontend_dir, html=True), name="frontend")

@app.get("/")
def root():
    return {
        "system": "TrendStyle Fashion & E-Commerce SOA Platform",
        "author": "Phạm Văn Thái - B25DTCN298",
        "docs_url": "/docs",
        "web_client": "/client/index.html"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
