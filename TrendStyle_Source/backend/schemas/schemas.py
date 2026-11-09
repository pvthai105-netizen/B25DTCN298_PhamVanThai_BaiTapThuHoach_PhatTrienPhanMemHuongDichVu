from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# --- Auth & User Schemas ---
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    full_name: str
    role: str

class UserProfile(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    phone: Optional[str]
    address: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class ChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)

# --- Category & Brand Schemas ---
class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class CategoryOut(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class BrandOut(BaseModel):
    id: int
    name: str
    slug: str
    origin: Optional[str] = None
    logo_url: Optional[str] = None
    class Config:
        from_attributes = True

# --- Product Schemas ---
class ProductBase(BaseModel):
    category_id: int
    brand_id: Optional[int] = None
    name: str
    slug: str
    sku: str
    price: float
    discount_price: Optional[float] = None
    stock_quantity: int = 0
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    gender: Optional[str] = "unisex"
    is_featured: Optional[bool] = False

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    is_featured: Optional[bool] = None

class ProductOut(ProductBase):
    id: int
    created_at: datetime
    avg_rating: Optional[float] = 5.0
    review_count: Optional[int] = 0
    category: Optional[CategoryOut] = None
    brand: Optional[BrandOut] = None

    class Config:
        from_attributes = True

# --- Cart Schemas ---
class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(1, ge=1)
    selected_size: Optional[str] = "M"
    selected_color: Optional[str] = "Default"

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)

class CartItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_thumbnail: Optional[str]
    price: float
    quantity: int
    selected_size: str
    selected_color: str
    subtotal: float

class CartOut(BaseModel):
    items: List[CartItemOut]
    total_quantity: int
    total_price: float

# --- Order Schemas ---
class OrderCreate(BaseModel):
    receiver_name: str
    receiver_phone: str
    shipping_address: str
    note: Optional[str] = None
    payment_method: str = "cod"

class OrderItemOut(BaseModel):
    product_id: int
    product_name: str
    product_thumbnail: Optional[str]
    quantity: int
    unit_price: float
    subtotal: float
    selected_size: str
    selected_color: str

class OrderOut(BaseModel):
    id: int
    order_code: str
    total_amount: float
    shipping_fee: float
    final_amount: float
    status: str
    receiver_name: str
    receiver_phone: str
    shipping_address: str
    note: Optional[str]
    payment_method: Optional[str]
    payment_status: Optional[str]
    created_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str

# --- Payment Schemas ---
class PaymentProcess(BaseModel):
    order_code: str
    payment_method: str
    mock_success: bool = True

class PaymentOut(BaseModel):
    order_code: str
    payment_method: str
    payment_status: str
    transaction_code: str
    message: str

# --- Review Schemas ---
class ReviewCreate(BaseModel):
    product_id: int
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = None
    comment: str

class ReviewOut(BaseModel):
    id: int
    product_id: int
    user_id: int
    user_name: str
    rating: int
    title: Optional[str]
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- News & Comment Schemas ---
class NewsCreate(BaseModel):
    title: str
    slug: str
    summary: str
    content: str
    thumbnail: Optional[str] = None
    category_tag: str = "Xu hướng mới"
    author: Optional[str] = "TrendStyle Editorial"

class NewsOut(BaseModel):
    id: int
    title: str
    slug: str
    summary: str
    content: str
    thumbnail: Optional[str]
    category_tag: str
    author: str
    view_count: int
    created_at: datetime
    comment_count: Optional[int] = 0

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    news_id: int
    content: str

class CommentOut(BaseModel):
    id: int
    news_id: int
    user_id: int
    user_name: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Admin Statistics ---
class AdminDashboardStats(BaseModel):
    total_users: int
    total_products: int
    total_orders: int
    total_revenue: float
    recent_orders: List[OrderOut] = []
