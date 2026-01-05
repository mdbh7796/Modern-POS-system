import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from data.database import SessionLocal, init_db
from data.models import Product, Order
import time

def verify():
    print("Starting verification...")
    
    # headless qapplication
    app = QApplication(sys.argv)
    
    try:
        init_db()
        window = MainWindow()
        
        db = SessionLocal()
        product = db.query(Product).first()
        
        if not product:
            print("FAILED: Seed data missing.")
            return

        print(f"Testing with product: {product.name} (${product.price})")
        
        # 1. Add to Cart
        window.add_to_cart_by_id(product.id)
        if len(window.cart_items) != 1:
            print("FAILED: Item not added to cart list.")
            return
            
        print("Cart Logic: OK")
        
        # 2. Checkout
        total = product.price
        print(f"Processing order for ${total}...")
        window.process_order(total)
        
        # 3. Verify DB
        latest_order = db.query(Order).order_by(Order.id.desc()).first()
        if latest_order and abs(latest_order.total_amount - total) < 0.01:
            print("Database Persistence: OK")
            print("VERIFICATION SUCCESSFUL")
        else:
            print("FAILED: Order not found in DB or amount mismatch.")
            
    except Exception as e:
        print(f"EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify()
