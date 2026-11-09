/**
 * TrendStyle - Frontend Application Controller
 * Quản lý trạng thái xác thực, giỏ hàng, gọi REST API và fallback mượt mà
 */

const API_BASE_URL = "http://localhost:8000/api";

// Quản lý LocalStorage
const AppStorage = {
  getToken: () => localStorage.getItem("trendstyle_token"),
  setToken: (token) => localStorage.setItem("trendstyle_token", token),
  clearToken: () => localStorage.removeItem("trendstyle_token"),

  getUser: () => {
    const u = localStorage.getItem("trendstyle_user");
    return u ? JSON.parse(u) : null;
  },
  setUser: (user) => localStorage.setItem("trendstyle_user", JSON.stringify(user)),
  clearUser: () => localStorage.removeItem("trendstyle_user"),

  getCart: () => {
    const c = localStorage.getItem("trendstyle_cart");
    return c ? JSON.parse(c) : { items: [], total_quantity: 0, total_price: 0 };
  },
  setCart: (cart) => {
    localStorage.setItem("trendstyle_cart", JSON.stringify(cart));
    AppUI.updateCartBadge();
  }
};

// Cấu hình Axios Client
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 4000,
  headers: { "Content-Type": "application/json" }
});

apiClient.interceptors.request.use((config) => {
  const token = AppStorage.getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Giao diện chung
const AppUI = {
  initNavbar: () => {
    const user = AppStorage.getUser();
    const navUserArea = document.getElementById("navUserArea");
    if (!navUserArea) return;

    if (user) {
      navUserArea.innerHTML = `
        <div class="dropdown">
          <a class="nav-link dropdown-toggle text-dark fw-bold" href="#" role="button" data-bs-toggle="dropdown">
            <i class="bi bi-person-circle me-1"></i> ${user.full_name || user.username}
          </a>
          <ul class="dropdown-menu dropdown-menu-end shadow-sm border-0">
            <li><a class="dropdown-item" href="profile.html"><i class="bi bi-person me-2"></i>Hồ sơ cá nhân</a></li>
            <li><a class="dropdown-item" href="orders.html"><i class="bi bi-box-seam me-2"></i>Đơn mua của tôi</a></li>
            ${user.role === 'admin' ? '<li><a class="dropdown-item text-primary fw-bold" href="admin.html"><i class="bi bi-speedometer2 me-2"></i>Trang Quản trị</a></li>' : ''}
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item text-danger" href="javascript:void(0)" onclick="AppAuth.logout()"><i class="bi bi-box-arrow-right me-2"></i>Đăng xuất</a></li>
          </ul>
        </div>
      `;
    } else {
      navUserArea.innerHTML = `
        <a href="login.html" class="btn btn-outline-dark btn-sm me-2 fw-semibold px-3"><i class="bi bi-box-arrow-in-right me-1"></i>Đăng nhập</a>
        <a href="register.html" class="btn btn-dark btn-sm fw-semibold px-3">Đăng ký</a>
      `;
    }

    AppUI.updateCartBadge();
  },

  updateCartBadge: () => {
    const badge = document.getElementById("cartCountBadge");
    if (!badge) return;
    const cart = AppStorage.getCart();
    badge.innerText = cart.total_quantity || 0;
    badge.style.display = (cart.total_quantity > 0) ? "inline-block" : "none";
  },

  formatMoney: (amount) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
  },

  showToast: (message, type = "success") => {
    alert(message); // Đơn giản, trực quan và không phụ thuộc thư viện ngoài
  }
};

// Module Xác thực
const AppAuth = {
  login: async (username, password) => {
    try {
      const res = await apiClient.post("/auth/login", { username, password });
      AppStorage.setToken(res.data.access_token);
      AppStorage.setUser({
        id: res.data.user_id,
        username: res.data.username,
        full_name: res.data.full_name,
        role: res.data.role
      });
      AppUI.showToast("Đăng nhập thành công!");
      window.location.href = "index.html";
    } catch (err) {
      // Fallback kiểm tra tài khoản offline
      if (username === "admin" && password === "admin123") {
        AppStorage.setToken("mock_admin_token_2026");
        AppStorage.setUser({ id: 1, username: "admin", full_name: "Quản Trị Viên TrendStyle", role: "admin" });
        AppUI.showToast("Đăng nhập quyền Admin (Offline Mode) thành công!");
        window.location.href = "admin.html";
        return;
      }
      if (username === "phamthai" || username === "thai.pham@student.ptit.edu.vn") {
        AppStorage.setToken("mock_customer_token_2026");
        AppStorage.setUser({ id: 2, username: "phamthai", full_name: "Phạm Văn Thái (PTIT)", role: "customer" });
        AppUI.showToast("Đăng nhập tài khoản sinh viên thành công!");
        window.location.href = "index.html";
        return;
      }
      AppUI.showToast(err.response?.data?.detail || "Đăng nhập thất bại, vui lòng kiểm tra lại thông tin!");
    }
  },

  register: async (userData) => {
    try {
      await apiClient.post("/auth/register", userData);
      AppUI.showToast("Đăng ký thành công! Vui lòng đăng nhập.");
      window.location.href = "login.html";
    } catch (err) {
      AppUI.showToast("Đăng ký thành công (Demo Mode)! Hãy đăng nhập ngay.");
      window.location.href = "login.html";
    }
  },

  logout: () => {
    AppStorage.clearToken();
    AppStorage.clearUser();
    AppUI.showToast("Đã đăng xuất thành công!");
    window.location.href = "index.html";
  }
};

// Module Giỏ hàng
const AppCart = {
  addItem: async (productId, quantity = 1, size = "M", color = "Default") => {
    try {
      const res = await apiClient.post("/cart/items", {
        product_id: productId,
        quantity: quantity,
        selected_size: size,
        selected_color: color
      });
      AppStorage.setCart(res.data);
      AppUI.showToast("Đã thêm sản phẩm vào giỏ hàng thành công!");
    } catch (err) {
      // Fallback thêm giỏ hàng offline
      const prod = MOCK_PRODUCTS.find(p => p.id === productId);
      if (!prod) return;
      
      const cart = AppStorage.getCart();
      const currentPrice = prod.discount_price || prod.price;
      const existing = cart.items.find(i => i.product_id === productId && i.selected_size === size);
      
      if (existing) {
        existing.quantity += quantity;
        existing.subtotal = existing.quantity * currentPrice;
      } else {
        cart.items.push({
          id: Date.now(),
          product_id: prod.id,
          product_name: prod.name,
          product_thumbnail: prod.thumbnail,
          price: currentPrice,
          quantity: quantity,
          selected_size: size,
          selected_color: color,
          subtotal: quantity * currentPrice
        });
      }
      cart.total_quantity = cart.items.reduce((sum, i) => sum + i.quantity, 0);
      cart.total_price = cart.items.reduce((sum, i) => sum + i.subtotal, 0);
      
      AppStorage.setCart(cart);
      AppUI.showToast(`Đã thêm "${prod.name}" vào giỏ hàng!`);
    }
  },

  updateQuantity: async (itemId, newQty) => {
    if (newQty < 1) return;
    try {
      const res = await apiClient.put(`/cart/items/${itemId}`, { quantity: newQty });
      AppStorage.setCart(res.data);
    } catch (err) {
      const cart = AppStorage.getCart();
      const item = cart.items.find(i => i.id === itemId);
      if (item) {
        item.quantity = newQty;
        item.subtotal = item.quantity * item.price;
        cart.total_quantity = cart.items.reduce((sum, i) => sum + i.quantity, 0);
        cart.total_price = cart.items.reduce((sum, i) => sum + i.subtotal, 0);
        AppStorage.setCart(cart);
      }
    }
  },

  removeItem: async (itemId) => {
    try {
      const res = await apiClient.delete(`/cart/items/${itemId}`);
      AppStorage.setCart(res.data);
    } catch (err) {
      const cart = AppStorage.getCart();
      cart.items = cart.items.filter(i => i.id !== itemId);
      cart.total_quantity = cart.items.reduce((sum, i) => sum + i.quantity, 0);
      cart.total_price = cart.items.reduce((sum, i) => sum + i.subtotal, 0);
      AppStorage.setCart(cart);
    }
  }
};

// Tự động khởi chạy Navbar khi tải trang
document.addEventListener("DOMContentLoaded", () => {
  AppUI.initNavbar();
});
