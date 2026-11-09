from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.entities import Cart, CartItem, Product
from schemas.schemas import CartItemAdd

class CartService:
    """Cart Service: Quản lý giỏ hàng, cập nhật số lượng và tính tổng tiền"""

    @staticmethod
    def get_user_cart(db: Session, user_id: int):
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        
        items_out = []
        total_quantity = 0
        total_price = 0.0

        for item in cart.items:
            prod = item.product
            current_price = prod.discount_price if prod.discount_price and prod.discount_price > 0 else prod.price
            subtotal = current_price * item.quantity
            
            items_out.append({
                "id": item.id,
                "product_id": prod.id,
                "product_name": prod.name,
                "product_thumbnail": prod.thumbnail,
                "price": current_price,
                "quantity": item.quantity,
                "selected_size": item.selected_size,
                "selected_color": item.selected_color,
                "subtotal": subtotal
            })
            total_quantity += item.quantity
            total_price += subtotal

        return {
            "items": items_out,
            "total_quantity": total_quantity,
            "total_price": total_price
        }

    @staticmethod
    def add_to_cart(db: Session, user_id: int, item_in: CartItemAdd):
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)

        # Kiểm tra sản phẩm và tồn kho
        prod = db.query(Product).filter(Product.id == item_in.product_id).first()
        if not prod:
            raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
        if prod.stock_quantity < item_in.quantity:
            raise HTTPException(status_code=400, detail="Số lượng trong kho không đủ đáp ứng")

        # Kiểm tra nếu đã có món hàng cùng size & màu
        existing_item = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == item_in.product_id,
            CartItem.selected_size == item_in.selected_size,
            CartItem.selected_color == item_in.selected_color
        ).first()

        if existing_item:
            new_qty = existing_item.quantity + item_in.quantity
            if prod.stock_quantity < new_qty:
                raise HTTPException(status_code=400, detail="Số lượng yêu cầu vượt quá tồn kho")
            existing_item.quantity = new_qty
        else:
            new_item = CartItem(
                cart_id=cart.id,
                product_id=item_in.product_id,
                quantity=item_in.quantity,
                selected_size=item_in.selected_size,
                selected_color=item_in.selected_color
            )
            db.add(new_item)

        db.commit()
        return CartService.get_user_cart(db, user_id)

    @staticmethod
    def update_cart_item(db: Session, user_id: int, cart_item_id: int, quantity: int):
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            raise HTTPException(status_code=404, detail="Không tìm thấy giỏ hàng")

        item = db.query(CartItem).filter(CartItem.id == cart_item_id, CartItem.cart_id == cart.id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Không tìm thấy món hàng trong giỏ")

        if item.product.stock_quantity < quantity:
            raise HTTPException(status_code=400, detail="Số lượng trong kho không đủ")

        item.quantity = quantity
        db.commit()
        return CartService.get_user_cart(db, user_id)

    @staticmethod
    def remove_cart_item(db: Session, user_id: int, cart_item_id: int):
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            raise HTTPException(status_code=404, detail="Không tìm thấy giỏ hàng")

        item = db.query(CartItem).filter(CartItem.id == cart_item_id, CartItem.cart_id == cart.id).first()
        if item:
            db.delete(item)
            db.commit()
        return CartService.get_user_cart(db, user_id)

    @staticmethod
    def clear_cart(db: Session, user_id: int):
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if cart:
            db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
            db.commit()
