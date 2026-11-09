/**
 * TrendStyle - Mock Database cho chế độ Offline Demo
 * Đảm bảo các trang web chạy mượt mà ngay cả khi chưa khởi động FastAPI server!
 */
const MOCK_CATEGORIES = [
  { id: 1, name: "Áo Sơ Mi & Áo Thun", slug: "ao-so-mi-ao-thun", image_url: "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500" },
  { id: 2, name: "Quần Jeans & Quần Tây", slug: "quan-jeans-quan-tay", image_url: "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500" },
  { id: 3, name: "Áo Khoác & Blazer", slug: "ao-khoac-blazer", image_url: "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500" },
  { id: 4, name: "Váy & Đầm Nữ", slug: "vay-dam-nu", image_url: "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500" },
  { id: 5, name: "Giày & Phụ Kiện", slug: "giay-phu-kien", image_url: "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500" }
];

const MOCK_PRODUCTS = [
  {
    id: 1,
    name: "Áo Blazer Linen Form Rộng Minimalist Beige",
    slug: "ao-blazer-linen-form-rong-beige",
    category_id: 3,
    category_name: "Áo Khoác & Blazer",
    price: 850000,
    discount_price: 720000,
    stock_quantity: 45,
    gender: "women",
    is_featured: true,
    thumbnail: "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600",
    description: "Áo blazer phom rộng phong cách tối giản màu be trang nhã. Chất liệu vải linen tự nhiên thoáng mát, thích hợp cả đi làm lẫn dạo phố cuối tuần.",
    avg_rating: 4.9,
    review_count: 18
  },
  {
    id: 2,
    name: "Áo Sơ Mi Oxford Cotton Regular Fit Trắng",
    slug: "ao-so-mi-oxford-cotton-trang",
    category_id: 1,
    category_name: "Áo Sơ Mi & Áo Thun",
    price: 490000,
    discount_price: 420000,
    stock_quantity: 60,
    gender: "men",
    is_featured: true,
    thumbnail: "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600",
    description: "Chất liệu 100% cotton Oxford dệt chéo mềm mại, cổ cài khuy cổ điển, giữ nếp phẳng phiu suốt ngày dài làm việc.",
    avg_rating: 4.8,
    review_count: 24
  },
  {
    id: 3,
    name: "Quần Tây Ống Suông Smart Casual Xám Tro",
    slug: "quan-tay-ong-suong-smart-casual-xam",
    category_id: 2,
    category_name: "Quần Jeans & Quần Tây",
    price: 550000,
    discount_price: 480000,
    stock_quantity: 38,
    gender: "unisex",
    is_featured: true,
    thumbnail: "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=600",
    description: "Thiết kế cạp cao ống suông che khuyết điểm hoàn hảo, co giãn nhẹ êm ái khi di chuyển, dễ dàng phối cùng blazer hoặc sơ mi.",
    avg_rating: 5.0,
    review_count: 12
  },
  {
    id: 4,
    name: "Đầm Lụa Midi Cổ Yếm Dự Tiệc Đen Quý Phái",
    slug: "dam-lua-midi-co-yem-den",
    category_id: 4,
    category_name: "Váy & Đầm Nữ",
    price: 980000,
    discount_price: 850000,
    stock_quantity: 25,
    gender: "women",
    is_featured: true,
    thumbnail: "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600",
    description: "Chất liệu lụa satin cao cấp bắt sáng tinh tế, đường cắt xẻ khéo léo mang lại vẻ đẹp quyến rũ và thanh lịch cho các buổi tiệc tối.",
    avg_rating: 4.9,
    review_count: 31
  },
  {
    id: 5,
    name: "Túi Xách Da Đeo Chéo Minimalist Nâu Caramel",
    slug: "tui-xach-da-deo-cheo-nau-caramel",
    category_id: 5,
    category_name: "Giày & Phụ Kiện",
    price: 620000,
    discount_price: 550000,
    stock_quantity: 50,
    gender: "women",
    is_featured: false,
    thumbnail: "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600",
    description: "Chất liệu da nhân tạo vi sợi chống xước, khoá kim loại mạ vàng sang trọng, kích thước vừa vặn đựng điện thoại và vật dụng cá nhân.",
    avg_rating: 4.7,
    review_count: 15
  },
  {
    id: 6,
    name: "Áo Thun Heavyweight Oversized Cotton 100% Đen",
    slug: "ao-thun-heavyweight-oversized-den",
    category_id: 1,
    category_name: "Áo Sơ Mi & Áo Thun",
    price: 320000,
    discount_price: 280000,
    stock_quantity: 80,
    gender: "unisex",
    is_featured: true,
    thumbnail: "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600",
    description: "Áo thun định lượng 260gsm đứng form dày dặn, bo cổ dệt kim chống giãn, phong cách Streetwear hiện đại trẻ trung.",
    avg_rating: 4.9,
    review_count: 42
  }
];

const MOCK_NEWS = [
  {
    id: 1,
    title: "Xu Hướng Phong Cách Minimalist: Nghệ Thuật Tinh Gọn Của Thập Kỷ Mới",
    slug: "xu-huong-minimalist-nghe-thuat-tinh-gon",
    summary: "Khám phá cách phong cách tối giản (Minimalism) định hình lại tủ quần áo của giới trẻ với các gam màu trung tính: đen, trắng, be và xám.",
    content: `
      <p>Phong cách tối giản (Minimalism) không đơn thuần là một trào lưu nhất thời, mà là một triết lý sống và phong cách cá nhân sâu sắc. Thay vì chạy theo số lượng, Minimalist hướng đến chất lượng của từng món trang phục và khả năng phối linh hoạt cao độ.</p>
      <h5>1. Bảng màu trung tính trường tồn với thời gian</h5>
      <p>Sự kết hợp giữa đen, trắng, màu be (beige), xám và nâu đất tạo nên tổng thể hài hòa, dịu mắt nhưng cực kỳ sang trọng. Những gam màu này không bao giờ lỗi mốt và có thể dễ dàng ghép nối với nhau trong mọi hoàn cảnh.</p>
      <h5>2. Phom dáng chuẩn mực và chất liệu tự nhiên</h5>
      <p>Một chiếc áo blazer may đo chuẩn chỉ từ vải linen hoặc wool pha, kết hợp cùng áo thun trắng trơn và quần tây ống suông cạp cao là công thức hoàn hảo để tự tin sải bước từ phòng họp đến những buổi gặp gỡ bạn bè.</p>
    `,
    thumbnail: "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800",
    category_tag: "Minimalist",
    author: "Minh Thư - TrendStyle Fashion Editor",
    created_at: "2026-11-01",
    view_count: 342,
    comment_count: 2
  },
  {
    id: 2,
    title: "Cẩm Nang Phối Đồ Thu Đông 2026: Đỉnh Cao Nghệ Thuật Layering",
    slug: "cam-nang-phoi-do-thu-dong-2026-layering",
    summary: "Bí quyết kết hợp các lớp trang phục vừa giữ ấm hiệu quả vừa thể hiện gu thẩm mỹ thời thượng mà không bị cồng kềnh.",
    content: `
      <p>Kỹ thuật Layering (xếp lớp trang phục) là chìa khóa vàng cho mùa lạnh. Để không biến mình thành một 'khối áo ấm di động', bạn cần nắm vững quy tắc 3 lớp cơ bản.</p>
      <h5>Lớp 1: Lớp nền mỏng nhẹ</h5>
      <p>Sử dụng áo giữ nhiệt, áo thun cotton mỏng ôm vừa vặn hoặc sơ mi cổ đức thanh lịch.</p>
      <h5>Lớp 2: Lớp cách nhiệt và tạo điểm nhấn</h5>
      <p>Áo len mỏng cổ tròn, cardigan đan len nhẹ, hoặc áo gile dạ.</p>
      <h5>Lớp 3: Lớp áo khoác ngoài</h5>
      <p>Một chiếc blazer phom rộng hoặc măng tô dạ dáng dài giúp cân bằng tỷ lệ cơ thể và tạo vẻ ngoài chuẩn phong cách Hàn Quốc.</p>
    `,
    thumbnail: "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800",
    category_tag: "Thu Đông",
    author: "Hoàng Nam - Style Consultant",
    created_at: "2026-11-02",
    view_count: 520,
    comment_count: 3
  },
  {
    id: 3,
    title: "Streetwear 2026: Sự Trỗi Dậy Của Phom Dáng Oversized & Chất Liệu Bền Vững",
    slug: "streetwear-2026-oversized-ben-vung",
    summary: "Thời trang đường phố tiếp tục khẳng định vị thế với các thiết kế phóng khoáng và thông điệp bảo vệ môi trường từ sợi cotton tái chế.",
    content: `
      <p>Streetwear ngày nay không chỉ dừng lại ở sự nổi loạn ngẫu hứng, mà ngày càng gắn liền với lối sống bền vững (Sustainable Fashion). Các thương hiệu hàng đầu đang chuyển dịch mạnh mẽ sang bông hữu cơ và sợi tái sinh.</p>
      <p>Phom dáng oversized với vai rơi tự do, kết hợp cùng quần túi hộp cargo và giày chunky sneaker tiếp tục là combo thống trị các bức ảnh street-style toàn cầu năm nay.</p>
    `,
    thumbnail: "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800",
    category_tag: "Streetwear",
    author: "Đội ngũ TrendStyle",
    created_at: "2026-11-03",
    view_count: 288,
    comment_count: 1
  }
];

const MOCK_REVIEWS = [
  { id: 1, product_id: 1, user_name: "Phạm Văn Thái", rating: 5, title: "Chất vải rất xịn sò", comment: "Áo blazer form đứng, đường may cực kỳ cẩn thận. Mặc đi làm ai cũng khen!", created_at: "2026-11-02" },
  { id: 2, product_id: 1, user_name: "Lê Minh Trang", rating: 5, title: "Đẹp xuất sắc", comment: "Màu be bên ngoài y hệt như hình mẫu chụp, giao hàng rất nhanh.", created_at: "2026-11-03" },
  { id: 3, product_id: 2, user_name: "Nguyễn Văn Hùng", rating: 5, title: "Rất đáng tiền", comment: "Vải oxford mặc rất thoáng, giặt máy không bị nhăn nhiều. Sẽ ủng hộ shop dài lâu.", created_at: "2026-11-03" }
];

const MOCK_COMMENTS = [
  { id: 1, news_id: 1, user_name: "Phạm Văn Thái", content: "Bài viết rất hữu ích! Mình áp dụng quy tắc phối màu be và trắng thấy phong cách nâng tầm hẳn.", created_at: "2026-11-02 14:20" },
  { id: 2, news_id: 1, user_name: "Thuỳ Dung", content: "Minimalist luôn là chân ái, gọn gàng mà không bao giờ lỗi mốt.", created_at: "2026-11-03 09:15" },
  { id: 3, news_id: 2, user_name: "Quốc Anh", content: "Cách layering này phối với boot chelsea thì tuyệt vời luôn ad ơi!", created_at: "2026-11-03 16:40" }
];
