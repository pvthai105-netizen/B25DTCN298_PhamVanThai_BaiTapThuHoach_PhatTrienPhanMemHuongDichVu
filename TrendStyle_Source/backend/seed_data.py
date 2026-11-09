from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models.entities import User, UserRole, Category, Brand, Product, News, Review, Comment, Cart
from services.auth_service import AuthService

def init_db_and_seed():
    """Khởi tạo bảng và nạp dữ liệu mẫu thời trang thực tế"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Tạo tài khoản mẫu
        if not db.query(User).filter(User.username == "admin").first():
            admin_user = User(
                username="admin",
                email="admin@trendstyle.vn",
                password_hash=AuthService.hash_password("admin123"),
                full_name="Quản Trị Viên TrendStyle",
                phone="0988888888",
                address="Học viện CNBCVT, Hà Nội",
                role=UserRole.ADMIN.value
            )
            db.add(admin_user)
            db.flush()
            db.add(Cart(user_id=admin_user.id))

        if not db.query(User).filter(User.username == "phamthai").first():
            customer_user = User(
                username="phamthai",
                email="thai.pham@student.ptit.edu.vn",
                password_hash=AuthService.hash_password("123456"),
                full_name="Phạm Văn Thái",
                phone="0912345678",
                address="Km10 Nguyễn Trãi, Hà Đông, Hà Nội",
                role=UserRole.CUSTOMER.value
            )
            db.add(customer_user)
            db.flush()
            db.add(Cart(user_id=customer_user.id))

        db.commit()

        # 2. Tạo danh mục thời trang
        categories_data = [
            {"name": "Áo Sơ Mi & Áo Thun", "slug": "ao-so-mi-ao-thun", "description": "Thời trang áo hiện đại, phong cách thanh lịch và năng động", "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500"},
            {"name": "Quần Jeans & Quần Tây", "slug": "quan-jeans-quan-tay", "description": "Dáng quần chuẩn form, tôn dáng, chất liệu cao cấp", "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500"},
            {"name": "Áo Khoác & Blazer", "slug": "ao-khoac-blazer", "description": "Blazer phong cách Hàn Quốc, áo khoác dạ, măng tô Thu Đông", "image_url": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500"},
            {"name": "Váy & Đầm Nữ", "slug": "vay-dam-nu", "description": "Đầm dạ hội, váy dạo phố thanh lịch và nữ tính", "image_url": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500"},
            {"name": "Giày & Phụ Kiện", "slug": "giay-phu-kien", "description": "Sneaker, giày da, túi xách, kính râm và thắt lưng", "image_url": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500"},
        ]
        
        cat_map = {}
        for c in categories_data:
            existing = db.query(Category).filter(Category.slug == c["slug"]).first()
            if not existing:
                cat = Category(**c)
                db.add(cat)
                db.flush()
                cat_map[c["slug"]] = cat.id
            else:
                cat_map[c["slug"]] = existing.id

        # 3. Tạo Thương hiệu thời trang
        brands_data = [
            {"name": "Zara", "slug": "zara", "origin": "Spain"},
            {"name": "Uniqlo", "slug": "uniqlo", "origin": "Japan"},
            {"name": "H&M", "slug": "hm", "origin": "Sweden"},
            {"name": "TrendStyle Studio", "slug": "trendstyle-studio", "origin": "Vietnam"}
        ]
        brand_map = {}
        for b in brands_data:
            existing = db.query(Brand).filter(Brand.slug == b["slug"]).first()
            if not existing:
                br = Brand(**b)
                db.add(br)
                db.flush()
                brand_map[b["slug"]] = br.id
            else:
                brand_map[b["slug"]] = existing.id

        db.commit()

        # 4. Tạo Sản phẩm thời trang
        if db.query(Product).count() == 0:
            products_data = [
                {
                    "category_id": cat_map["ao-khoac-blazer"],
                    "brand_id": brand_map["zara"],
                    "name": "Áo Blazer Linen Form Rộng Minimalist Beige",
                    "slug": "ao-blazer-linen-form-rong-beige",
                    "sku": "TS-BLZ-001",
                    "price": 850000,
                    "discount_price": 720000,
                    "stock_quantity": 45,
                    "description": "Áo blazer phom rộng phong cách tối giản màu be trang nhã. Chất liệu vải linen tự nhiên thoáng mát, thích hợp cả đi làm lẫn dạo phố cuối tuần.",
                    "thumbnail": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600",
                    "gender": "women",
                    "is_featured": True
                },
                {
                    "category_id": cat_map["ao-so-mi-ao-thun"],
                    "brand_id": brand_map["uniqlo"],
                    "name": "Áo Sơ Mi Oxford Cotton Regular Fit Trắng",
                    "slug": "ao-so-mi-oxford-cotton-trang",
                    "sku": "TS-SMI-002",
                    "price": 490000,
                    "discount_price": 420000,
                    "stock_quantity": 60,
                    "description": "Chất liệu 100% cotton Oxford dệt chéo mềm mại, cổ cài khuy cổ điển, giữ nếp phẳng phiu suốt ngày dài làm việc.",
                    "thumbnail": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600",
                    "gender": "men",
                    "is_featured": True
                },
                {
                    "category_id": cat_map["quan-jeans-quan-tay"],
                    "brand_id": brand_map["hm"],
                    "name": "Quần Tây Ống Suông Smart Casual Xám Tro",
                    "slug": "quan-tay-ong-suong-smart-casual-xam",
                    "sku": "TS-PNT-003",
                    "price": 550000,
                    "discount_price": 480000,
                    "stock_quantity": 38,
                    "description": "Thiết kế cạp cao ống suông che khuyết điểm hoàn hảo, co giãn nhẹ êm ái khi di chuyển, dễ dàng phối cùng blazer hoặc sơ mi.",
                    "thumbnail": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=600",
                    "gender": "unisex",
                    "is_featured": True
                },
                {
                    "category_id": cat_map["vay-dam-nu"],
                    "brand_id": brand_map["trendstyle-studio"],
                    "name": "Đầm Lụa Midi Cổ Yếm Dự Tiệc Đen Quý Phái",
                    "slug": "dam-lua-midi-co-yem-den",
                    "sku": "TS-DRS-004",
                    "price": 980000,
                    "discount_price": 850000,
                    "stock_quantity": 25,
                    "description": "Chất liệu lụa satin cao cấp bắt sáng tinh tế, đường cắt xẻ khéo léo mang lại vẻ đẹp quyến rũ và thanh lịch cho các buổi tiệc tối.",
                    "thumbnail": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600",
                    "gender": "women",
                    "is_featured": True
                },
                {
                    "category_id": cat_map["giay-phu-kien"],
                    "brand_id": brand_map["trendstyle-studio"],
                    "name": "Túi Xách Da Đeo Chéo Minimalist Nâu Caramel",
                    "slug": "tui-xach-da-deo-cheo-nau-caramel",
                    "sku": "TS-BAG-005",
                    "price": 620000,
                    "discount_price": 550000,
                    "stock_quantity": 50,
                    "description": "Chất liệu da nhân tạo vi sợi chống xước, khoá kim loại mạ vàng sang trọng, kích thước vừa vặn đựng điện thoại và vật dụng cá nhân.",
                    "thumbnail": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600",
                    "gender": "women",
                    "is_featured": False
                },
                {
                    "category_id": cat_map["ao-so-mi-ao-thun"],
                    "brand_id": brand_map["trendstyle-studio"],
                    "name": "Áo Thun Heavyweight Oversized Cotton 100% Đen",
                    "slug": "ao-thun-heavyweight-oversized-den",
                    "sku": "TS-TSH-006",
                    "price": 320000,
                    "discount_price": 280000,
                    "stock_quantity": 80,
                    "description": "Áo thun định lượng 260gsm đứng form dày dặn, bo cổ dệt kim chống giãn, phong cách Streetwear hiện đại trẻ trung.",
                    "thumbnail": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600",
                    "gender": "unisex",
                    "is_featured": True
                }
            ]

            created_prods = []
            for p in products_data:
                prod = Product(**p)
                db.add(prod)
                db.flush()
                created_prods.append(prod)

            # Thêm đánh giá mẫu
            thai_user = db.query(User).filter(User.username == "phamthai").first()
            if thai_user and created_prods:
                db.add(Review(
                    product_id=created_prods[0].id,
                    user_id=thai_user.id,
                    rating=5,
                    title="Chất vải rất xịn sò",
                    comment="Áo blazer form đứng, đường may cực kỳ cẩn thận. Mặc đi làm ai cũng khen!"
                ))
                db.add(Review(
                    product_id=created_prods[1].id,
                    user_id=thai_user.id,
                    rating=5,
                    title="Rất đáng tiền",
                    comment="Vải oxford mặc rất thoáng, giặt máy không bị nhăn nhiều. Mình sẽ ủng hộ tiếp."
                ))

        # 5. Tạo Bài viết Xu hướng Thời trang
        if db.query(News).count() == 0:
            news_data = [
                {
                    "title": "Xu Hướng Phong Cách Minimalist: Nghệ Thuật Tinh Gọn Của Thập Kỷ Mới",
                    "slug": "xu-huong-minimalist-nghe-thuat-tinh-gon",
                    "summary": "Khám phá cách phong cách tối giản (Minimalism) định hình lại tủ quần áo của giới trẻ với các gam màu trung tính: đen, trắng, be và xám.",
                    "content": "Phong cách tối giản không đơn thuần là mặc ít đi, mà là tập trung vào chất lượng, phom dáng và khả năng phối linh hoạt. Một chiếc áo blazer màu be, một chiếc quần tây ống suông và đôi sneaker trắng có thể đồng hành cùng bạn trong mọi hoàn cảnh...",
                    "thumbnail": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=700",
                    "category_tag": "Minimalist",
                    "author": "Minh Thư - TrendStyle Fashion Editor",
                    "view_count": 342
                },
                {
                    "title": "Cẩm Nang Phối Đồ Thu Đông 2026: Đỉnh Cao Nghệ Thuật Layering",
                    "slug": "cam-nang-phoi-do-thu-dong-2026-layering",
                    "summary": "Bí quyết kết hợp các lớp trang phục vừa giữ ấm hiệu quả vừa thể hiện gu thẩm mỹ thời thượng mà không bị cồng kềnh.",
                    "content": "Kỹ thuật Layering (xếp lớp trang phục) là chìa khóa vàng cho mùa lạnh. Hãy bắt đầu từ lớp nền mỏng nhẹ như áo giữ nhiệt hoặc sơ mi cotton, thêm một lớp len mỏng cổ tròn hoặc cardigan, và hoàn thiện bằng áo khoác dạ hoặc blazer phom rộng...",
                    "thumbnail": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=700",
                    "category_tag": "Thu Đông",
                    "author": "Hoàng Nam - Style Consultant",
                    "view_count": 520
                },
                {
                    "title": "Streetwear 2026: Sự Trỗi Dậy Của Phom Dáng Oversized & Chất Liệu Bền Vững",
                    "slug": "streetwear-2026-oversized-ben-vung",
                    "summary": "Thời trang đường phố tiếp tục khẳng định vị thế với các thiết kế phóng khoáng và thông điệp bảo vệ môi trường từ sợi cotton tái chế.",
                    "content": "Streetwear không chỉ là văn hóa mà còn là tuyên ngôn cá tính của thế hệ trẻ. Sự kết hợp giữa áo thun định lượng cao heavyweight, quần túi hộp cargo và giày sneaker thể thao tạo nên diện mạo cuốn hút, tự do...",
                    "thumbnail": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=700",
                    "category_tag": "Streetwear",
                    "author": "Đội ngũ TrendStyle",
                    "view_count": 288
                }
            ]

            created_news = []
            for n in news_data:
                article = News(**n)
                db.add(article)
                db.flush()
                created_news.append(article)

            # Thêm bình luận mẫu
            thai_user = db.query(User).filter(User.username == "phamthai").first()
            if thai_user and created_news:
                db.add(Comment(
                    news_id=created_news[0].id,
                    user_id=thai_user.id,
                    content="Bài viết rất hữu ích! Mình áp dụng quy tắc phối màu be và trắng thấy phong cách nâng tầm hẳn."
                ))
                db.add(Comment(
                    news_id=created_news[1].id,
                    user_id=thai_user.id,
                    content="Mùa đông năm nay mình nhất định sẽ thử cách phối layering này, cảm ơn tác giả!"
                ))

        db.commit()
        print("Database initialized and sample data seeded successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db_and_seed()
