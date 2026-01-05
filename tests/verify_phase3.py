import sys
import os
import shutil
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from PyQt6.QtWidgets import QApplication
from ui.login_window import LoginWindow
from controllers.product_controller import ProductController
from controllers.order_controller import OrderController
from data.database import init_db, SessionLocal
from data.models import User, Product

def verify_phase_3():
    print("Starting Phase 3 verification...")
    
    app = QApplication(sys.argv)
    
    # 1. Test Authentication
    print("Testing Authentication...")
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if admin and admin.password_hash == "admin123":
         print("Auth: Admin user exists and password matches.")
    else:
         print("FAILED: Admin user check.")
    db.close()
    
    # 2. Test Inventory Management
    print("Testing Inventory...")
    p_ctrl = ProductController()
    cat_id = p_ctrl.get_all_categories()[0].id
    new_prod = p_ctrl.add_product("StockTest", 1.00, cat_id)
    # Manually set stock
    db = SessionLocal()
    prod_db = db.query(Product).get(new_prod.id)
    prod_db.stock_quantity = 5
    db.commit()
    db.close()
    
    o_ctrl = OrderController()
    
    # Buy 5 (Stock 5 -> 0)
    try:
        o_ctrl.create_order([{'product': prod_db, 'qty': 5}], 5.00)
        print("Inventory: Bought 5 items (Stock should be 0)")
    except Exception as e:
        print(f"FAILED: Buying items failed: {e}")
        
    # Buy 1 (Stock 0 -> Fail)
    try:
        o_ctrl.create_order([{'product': prod_db, 'qty': 1}], 1.00)
        print("FAILED: Should have raised exception for out of stock.")
    except Exception as e:
        if "Insufficient stock" in str(e):
             print("Inventory: Blocked out of stock purchase OK")
        else:
             print(f"FAILED: Unexpected exception: {e}")
             
    # Cleanup
    p_ctrl.delete_product(new_prod.id)
    p_ctrl.close()
    o_ctrl.close()

    print("PHASE 3 VERIFICATION COMPLETE")

if __name__ == "__main__":
    verify_phase_3()
