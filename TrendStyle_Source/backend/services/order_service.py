import random
import string
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.entities import Order, OrderItem, OrderStatus, Payment, PaymentStatus, Cart, Product
from schemas.schemas import OrderCreate

class OrderService:
    """Order Service: Quản lý quy trình đặt hàng, trừ tồn kho, tính phí vận chuyển và cập nhật trạng thái đơn"""

    @staticmethod
    def generate_order_code() -> str:
        """Sinh mã đơn hàng độc nhất dạng TS-YYYYMMDD-XXXX"""
        date_str = datetime.utcnow().strftime("%Y%m%d")
        rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"TS-{date_str}-{rand_str}"

    @staticmethod
    def create_order(db: Session, user_id: int, order_in: OrderCreate) -> Order:
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart or not cart.items:
            raise HTTPException(status_code=400, detail="Giỏ hàng của bạn đang trống")

        total_amount = 0.0
        order_items_to_create = []

        # Kiểm tra tồn kho và chuẩn bị chi tiết đơn
        for item in cart.items:
            prod = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
            if not prod or prod.stock_quantity < item.quantity:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Sản phẩm {prod.name if prod else ''} không đủ số lượng trong kho"
                )

            # Khấu trừ số lượng tồn kho theo nguyên tắc giao dịch
            prod.stock_quantity -= item.quantity
            
            unit_price = prod.discount_price if prod.discount_price and prod.discount_price > 0 else prod.price
            subtotal = unit_price * item.quantity
            total_amount += subtotal

            order_items_to_create.append({
                "product_id": prod.id,
                "quantity": item.quantity,
                "unit_price": unit_price,
                "subtotal": subtotal,
                "selected_size": item.selected_size,
                "selected_color": item.selected_color
            })

        shipping_fee = 0.0 if total_amount >= 500000 else 30000.0  # Miễn phí ship cho đơn từ 500k
        final_amount = total_amount + shipping_fee

        new_order = Order(
            order_code=OrderService.generate_order_code(),
            user_id=user_id,
            total_amount=total_amount,
            shipping_fee=shipping_fee,
            final_amount=final_amount,
            status=OrderStatus.PENDING.value,
            receiver_name=order_in.receiver_name,
            receiver_phone=order_in.receiver_phone,
            shipping_address=order_in.shipping_address,
            note=order_in.note
        )
        db.add(new_order)
        db.flush()

        # Tạo Order Items
        for item_data in order_items_to_create:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                subtotal=item_data["subtotal"],
                selected_size=item_data["selected_size"],
                selected_color=item_data["selected_color"]
            )
            db.add(order_item)

        # Tạo bản ghi Thanh toán liên kết
        payment = Payment(
            order_id=new_order.id,
            payment_method=order_in.payment_method,
            payment_status=PaymentStatus.UNPAID.value
        )
        db.add(payment)

        # Xóa sạch giỏ hàng sau khi đặt thành công
        for item in cart.items:
            db.delete(item)

        db.commit()
        db.refresh(new_order)
        return new_order

    @staticmethod
    def get_user_orders(db: Session, user_id: int):
        return db.query(Order).filter(Order.user_id == user_id).order_by(Order.id.desc()).all()

    @staticmethod
    def get_order_by_code(db: Session, order_code: str):
        order = db.query(Order).filter(Order.order_code == order_code).first()
        if not order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
        return order

    @staticmethod
    def update_order_status(db: Session, order_id: int, new_status: str) -> Order:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
        order.status = new_status
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def cancel_order(db: Session, user_id: int, order_id: int) -> Order:
        order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
        if order.status not in [OrderStatus.PENDING.value, OrderStatus.CONFIRMED.value]:
            raise HTTPException(status_code=400, detail="Không thể hủy đơn hàng đang giao hoặc đã hoàn tất")

        # Hoàn trả lại số lượng tồn kho
        for item in order.items:
            prod = db.query(Product).filter(Product.id == item.product_id).first()
            if prod:
                prod.stock_quantity += item.quantity

        order.status = OrderStatus.CANCELLED.value
        db.commit()
        db.refresh(order)
        return order
