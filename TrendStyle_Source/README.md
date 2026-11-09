# TrendStyle - Nền Tảng Thời Trang & Thương Mại Điện Tử Hướng Dịch Vụ (SOA)

**Môn học:** Phát triển phần mềm hướng dịch vụ (Service-Oriented Software Development)  
**Học viện:** Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
**Sinh viên thực hiện:** Phạm Văn Thái  
**Mã sinh viên:** B25DTCN298  
**Lớp:** D25TXCN08-B  

---

## 1. Giới thiệu tổng quan
Hệ thống **TrendStyle** được xây dựng theo kiến trúc hướng dịch vụ (**SOA - Service-Oriented Architecture**), phân rã thành **10 dịch vụ nghiệp vụ độc lập**:
1. `Authentication Service`: Xác thực JWT, đăng ký, đăng nhập.
2. `User Service`: Quản lý tài khoản và hồ sơ người dùng.
3. `Product Service`: Danh mục, tìm kiếm, phân loại thời trang.
4. `Cart Service`: Thêm món, tính tổng tiền, quản lý giỏ hàng.
5. `Order Service`: Khấu trừ tồn kho, tính phí ship, tạo mã đơn hàng.
6. `Payment Service`: Xử lý thanh toán mô phỏng (COD, VNPAY, MoMo, VietQR).
7. `Review Service`: Đánh giá 1-5 sao và nhận xét sản phẩm.
8. `News Service`: Quản lý bài viết xu hướng, tạp chí thời trang.
9. `Comment Service`: Độc giả thảo luận, bình luận tin tức.
10. `Admin Service`: Thống kê doanh thu, đơn hàng, người dùng.

---

## 2. Cách chạy ứng dụng

### Cách 1: Chạy trực tiếp giao diện Frontend (Không cần cài đặt gì, chạy ngay tức thì)
1. Truy cập thư mục `BTTH/TrendStyle_Source/frontend/`.
2. Nhấp đúp chuột mở file `index.html` bằng bất kỳ trình duyệt nào (Chrome, Edge, Firefox).
3. Hệ thống tích hợp sẵn **Mock Data Store** thông minh, cho phép bạn trải nghiệm 100% tính năng (Đăng nhập, Thêm giỏ hàng, Đặt hàng, Đánh giá sản phẩm, Bình luận tin tức, Quản trị Admin) mượt mà!

### Cách 2: Khởi chạy Full-stack với Backend FastAPI (RESTful API + Swagger Docs)
1. Mở Terminal / PowerShell tại thư mục `BTTH/TrendStyle_Source/backend/`:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```
2. Mở trình duyệt xem tài liệu API chuẩn quốc tế Swagger UI:
   `http://localhost:8000/docs`
3. Truy cập giao diện Website kết nối trực tiếp API Backend:
   `http://localhost:8000/client/index.html`

---

## 3. Tài khoản demo có sẵn
- **Khách hàng:** `phamthai` | Mật khẩu: `123456`
- **Quản trị viên:** `admin` | Mật khẩu: `admin123`
