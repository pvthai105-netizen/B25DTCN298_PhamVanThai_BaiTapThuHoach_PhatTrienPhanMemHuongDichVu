from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from models.entities import User
from schemas.schemas import (
    UserRegister, UserLogin, TokenResponse, UserProfile, UserUpdate, ChangePassword,
    ProductCreate, ProductUpdate, ProductOut, CategoryOut, BrandOut,
    CartItemAdd, CartItemUpdate, CartOut,
    OrderCreate, OrderOut, OrderStatusUpdate,
    PaymentProcess, PaymentOut,
    ReviewCreate, ReviewOut,
    NewsCreate, NewsOut, CommentCreate, CommentOut,
    AdminDashboardStats
)
from services import (
    AuthService, UserService, ProductService, CartService, 
    OrderService, PaymentService, ReviewService, NewsService, 
    CommentService, AdminService
)
from routers.dependencies import get_current_user, require_admin

# 1. Auth Router
auth_router = APIRouter(prefix="/api/auth", tags=["1. Authentication Service"])

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user = AuthService.register_user(db, user_data)
    return {"message": "Đăng ký tài khoản thành công", "user_id": user.id, "username": user.username}

@auth_router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    return AuthService.authenticate_user(db, login_data)

@auth_router.get("/me", response_model=UserProfile)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


# 2. User Router
user_router = APIRouter(prefix="/api/users", tags=["2. User Service"])

@user_router.put("/profile", response_model=UserProfile)
def update_profile(data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return UserService.update_profile(db, current_user.id, data)

@user_router.post("/change-password")
def change_password(data: ChangePassword, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    UserService.change_password(db, current_user.id, data)
    return {"message": "Đổi mật khẩu thành công"}


# 3. Product Router
product_router = APIRouter(prefix="/api/products", tags=["3. Product Service"])

@product_router.get("", response_model=List[ProductOut])
def list_products(
    category_id: Optional[int] = None,
    brand_id: Optional[int] = None,
    gender: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    keyword: Optional[str] = None,
    is_featured: Optional[bool] = None,
    limit: int = 50,
    skip: int = 0,
    db: Session = Depends(get_db)
):
    return ProductService.get_all_products(
        db, category_id, brand_id, gender, min_price, max_price, keyword, is_featured, limit, skip
    )

@product_router.get("/categories", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return ProductService.get_categories(db)

@product_router.get("/brands", response_model=List[BrandOut])
def get_brands(db: Session = Depends(get_db)):
    return ProductService.get_brands(db)

@product_router.get("/{product_id}", response_model=ProductOut)
def get_product_detail(product_id: int, db: Session = Depends(get_db)):
    return ProductService.get_product_by_id(db, product_id)

@product_router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return ProductService.create_product(db, data)

@product_router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return ProductService.update_product(db, product_id, data)

@product_router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    ProductService.delete_product(db, product_id)
    return {"message": "Đã xóa sản phẩm thành công"}


# 4. Cart Router
cart_router = APIRouter(prefix="/api/cart", tags=["4. Cart Service"])

@cart_router.get("", response_model=CartOut)
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CartService.get_user_cart(db, current_user.id)

@cart_router.post("/items", response_model=CartOut)
def add_item_to_cart(item: CartItemAdd, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CartService.add_to_cart(db, current_user.id, item)

@cart_router.put("/items/{item_id}", response_model=CartOut)
def update_item_quantity(item_id: int, data: CartItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CartService.update_cart_item(db, current_user.id, item_id, data.quantity)

@cart_router.delete("/items/{item_id}", response_model=CartOut)
def remove_item_from_cart(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CartService.remove_cart_item(db, current_user.id, item_id)


# 5. Order Router
order_router = APIRouter(prefix="/api/orders", tags=["5. Order Service"])

@order_router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return OrderService.create_order(db, current_user.id, order_data)

@order_router.get("/my-orders", response_model=List[OrderOut])
def get_my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return OrderService.get_user_orders(db, current_user.id)

@order_router.get("/{order_code}", response_model=OrderOut)
def get_order_by_code(order_code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = OrderService.get_order_by_code(db, order_code)
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Bạn không có quyền xem đơn hàng này")
    return order

@order_router.put("/{order_id}/cancel", response_model=OrderOut)
def cancel_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return OrderService.cancel_order(db, current_user.id, order_id)

@order_router.put("/{order_id}/status", response_model=OrderOut)
def update_order_status(order_id: int, data: OrderStatusUpdate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return OrderService.update_order_status(db, order_id, data.status)


# 6. Payment Router
payment_router = APIRouter(prefix="/api/payments", tags=["6. Payment Service"])

@payment_router.post("/process", response_model=PaymentOut)
def process_payment(data: PaymentProcess, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return PaymentService.process_payment(db, data.order_code, data.payment_method, data.mock_success)


# 7. Review Router
review_router = APIRouter(prefix="/api/reviews", tags=["7. Review Service"])

@review_router.get("/product/{product_id}", response_model=List[ReviewOut])
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    return ReviewService.get_product_reviews(db, product_id)

@review_router.post("", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def submit_review(review_data: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ReviewService.create_review(db, current_user.id, review_data)

@review_router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    is_admin = (current_user.role == "admin")
    ReviewService.delete_review(db, current_user.id, review_id, is_admin)
    return {"message": "Đã xóa đánh giá thành công"}


# 8. News Router
news_router = APIRouter(prefix="/api/news", tags=["8. News Service"])

@news_router.get("", response_model=List[NewsOut])
def list_news(
    category_tag: Optional[str] = None,
    keyword: Optional[str] = None,
    limit: int = 20,
    skip: int = 0,
    db: Session = Depends(get_db)
):
    return NewsService.get_all_news(db, category_tag, keyword, limit, skip)

@news_router.get("/{news_id}", response_model=NewsOut)
def get_news_detail(news_id: int, db: Session = Depends(get_db)):
    return NewsService.get_news_by_id(db, news_id)

@news_router.post("", response_model=NewsOut, status_code=status.HTTP_201_CREATED)
def create_news(data: NewsCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return NewsService.create_news(db, data)

@news_router.delete("/{news_id}")
def delete_news(news_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    NewsService.delete_news(db, news_id)
    return {"message": "Đã xóa bài viết thành công"}


# 9. Comment Router
comment_router = APIRouter(prefix="/api/comments", tags=["9. Comment Service"])

@comment_router.get("/news/{news_id}", response_model=List[CommentOut])
def get_news_comments(news_id: int, db: Session = Depends(get_db)):
    return CommentService.get_news_comments(db, news_id)

@comment_router.post("", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def add_comment(data: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CommentService.create_comment(db, current_user.id, data)

@comment_router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    is_admin = (current_user.role == "admin")
    CommentService.delete_comment(db, current_user.id, comment_id, is_admin)
    return {"message": "Đã xóa bình luận thành công"}


# 10. Admin Router
admin_router = APIRouter(prefix="/api/admin", tags=["10. Admin Service"])

@admin_router.get("/stats", response_model=AdminDashboardStats)
def get_stats(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return AdminService.get_dashboard_statistics(db)
