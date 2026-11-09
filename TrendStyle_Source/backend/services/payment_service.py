import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.entities import Order, Payment, PaymentStatus

class PaymentService:
    """Payment Service: Xử lý thanh toán mô phỏng (COD, VNPAY, MoMo, Chuyển khoản ngân hàng)"""

    @staticmethod
    def process_payment(db: Session, order_code: str, payment_method: str, mock_success: bool = True):
        order = db.query(Order).filter(Order.order_code == order_code).first()
        if not order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng cần thanh toán")

        payment = db.query(Payment).filter(Payment.order_id == order.id).first()
        if not payment:
            payment = Payment(order_id=order.id)
            db.add(payment)

        payment.payment_method = payment_method

        if mock_success:
            payment.payment_status = PaymentStatus.PAID.value
            payment.transaction_code = f"TXN-{uuid.uuid4().hex[:10].upper()}"
            payment.paid_at = datetime.utcnow()
            message = f"Thanh toán đơn hàng {order_code} thành công qua {payment_method.upper()}"
        else:
            payment.payment_status = PaymentStatus.FAILED.value
            message = "Giao dịch thanh toán không thành công"

        db.commit()
        db.refresh(payment)

        return {
            "order_code": order_code,
            "payment_method": payment.payment_method,
            "payment_status": payment.payment_status,
            "transaction_code": payment.transaction_code or "",
            "message": message
        }
