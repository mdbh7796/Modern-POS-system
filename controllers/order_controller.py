from data.database import SessionLocal
from data.models import Order, OrderItem, OrderStatus, Product, Customer
from datetime import datetime

class OrderController:
    def __init__(self):
        self.db = SessionLocal()

    def create_order(self, cart_items, total_amount, customer_id=None):
        """
        cart_items: List of dict {'product': ProductObj, 'qty': int}
        """
        try:
            new_order = Order(
                total_amount=total_amount,
                status=OrderStatus.COMPLETED,
                timestamp=datetime.now(),
                customer_id=customer_id
            )
            self.db.add(new_order)
            self.db.commit()
            
            # Points Logic (1 point per whole dollar)
            if customer_id:
                points = int(total_amount)
                customer = self.db.query(Customer).get(customer_id)
                if customer:
                    customer.points += points
            
            for item in cart_items:
                product = item['product']
                
                # Refresh product from DB to get current stock and lock row (simplified)
                db_product = self.db.query(Product).with_for_update().get(product.id)
                
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
