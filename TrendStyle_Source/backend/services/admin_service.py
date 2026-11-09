from sqlalchemy.orm import Session
from sqlalchemy import func
from models.entities import User, Product, Order, OrderStatus

class AdminService:
    """Admin Service: Thống kê hiệu suất kinh doanh, doanh thu, đơn hàng và lượng người dùng"""

    @staticmethod
    def get_dashboard_statistics(db: Session):
        total_users = db.query(func.count(User.id)).scalar() or 0
        total_products = db.query(func.count(Product.id)).scalar() or 0
        total_orders = db.query(func.count(Order.id)).scalar() or 0
        
        # Doanh thu tính trên các đơn hàng không bị hủy
        total_revenue = db.query(func.sum(Order.final_amount))\
                          .filter(Order.status != OrderStatus.CANCELLED.value)\
                          .scalar() or 0.0

        recent_orders = db.query(Order).order_by(Order.id.desc()).limit(10).all()

        return {
            "total_users": total_users,
            "total_products": total_products,
            "total_orders": total_orders,
            "total_revenue": round(float(total_revenue), 2),
            "recent_orders": recent_orders
        }
