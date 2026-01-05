import sys
import os
import shutil

# Add project root to path
sys.path.append(os.getcwd())

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from controllers.product_controller import ProductController
from controllers.order_controller import OrderController
from data.database import init_db

def verify_phase_2():
    print("Starting Phase 2 verification...")
    
    app = QApplication(sys.argv)
    init_db()
    
    # 1. Test Refactoring (Controllers)
    print("Testing Controllers...")
    p_ctrl = ProductController()
    cats = p_ctrl.get_all_categories()
    if not cats:
        print("FAILED: No categories found (Refactoring check).")
        return
    print(f"ProductController: OK ({len(cats)} categories)")
    p_ctrl.close()
    
    # 2. Test Admin Feature (Product Management)
    print("Testing Admin Feature...")
    p_ctrl = ProductController()
    test_name = "Admin_Test_Prd"
    new_prod = p_ctrl.add_product(test_name, 9.99, cats[0].id)
    if new_prod.id:
        print("Admin: Add Product OK")
        # cleanup
        p_ctrl.delete_product(new_prod.id)
        print("Admin: Delete Product OK")
    else:
        print("FAILED: Admin Add Product")
    p_ctrl.close()
    
    # 3. Test Receipt Generation
    print("Testing Receipt Generation...")
    window = MainWindow()
    
    # Add item
    p_ctrl = ProductController()
    prod = p_ctrl.get_products_by_category(cats[0].id)[0]
    p_ctrl.close()
    
    window.cart_items = [{'product': prod, 'qty': 2}]
    
    # Use internal method to simulate order processing
    try:
        # Check if receipts dir is empty or note count
        if os.path.exists("receipts"):
            initial_count = len(os.listdir("receipts"))
        else:
            initial_count = 0
            
        print("Processing order...")
        window.process_order(prod.price * 2)
        
        final_count = len(os.listdir("receipts"))
        if final_count > initial_count:
            print("Receipt Generation: OK")
        else:
            print("FAILED: Receipt file not created.")
            
    except Exception as e:
        print(f"FAILED: Exception during order processing: {e}")
        import traceback
        traceback.print_exc()

    print("PHASE 2 VERIFICATION COMPLETE")

if __name__ == "__main__":
    verify_phase_2()
