from data.database import SessionLocal
from data.models import Order, OrderItem, OrderStatus, Product
from datetime import datetime

class OrderController:
    def __init__(self):
        self.db = SessionLocal()

    def create_order(self, cart_items, total_amount):
        """
        cart_items: List of dict {'product': ProductObj, 'qty': int}
        """
        try:
            new_order = Order(
                total_amount=total_amount,
                status=OrderStatus.COMPLETED,
                timestamp=datetime.now()
            )
            self.db.add(new_order)
            self.db.commit()
            
            for item in cart_items:
                product = item['product']
                
                # Refresh product from DB to get current stock and lock row
                db_product = self.db.get(Product, product.id, with_for_update=True)
                
                if db_product.stock_quantity < item['qty']:
                    raise Exception(f"Insufficient stock for {product.name}. Available: {db_product.stock_quantity}")
                
                db_product.stock_quantity -= item['qty']
                
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=product.id,
                    quantity=item['qty'],
                    price_at_time=product.price
                )
                self.db.add(order_item)
                
            self.db.commit()
            return new_order
        except Exception as e:
            self.db.rollback()
            raise e

    def get_order_history(self):
        return self.db.query(Order).order_by(Order.timestamp.desc()).all()

    def close(self):
        self.db.close()
