import sys
import os
sys.path.append(os.getcwd())

from data.database import SessionLocal, init_db
from data.models import Customer
from controllers.customer_controller import CustomerController
from controllers.order_controller import OrderController
from controllers.product_controller import ProductController

def verify_phase_4():
    print("Starting Phase 4 verification...")
    
    # 1. Test Customer Creation
    cust_ctrl = CustomerController()
    phone = "555-0199"
    # Clean up previous runs
    db = SessionLocal()
    existing = db.query(Customer).filter(Customer.phone == phone).first()
    if existing:
        db.delete(existing)
        db.commit()
    db.close()
    
    cust = cust_ctrl.create_customer(phone, "Test Customer")
    if cust and cust.phone == phone:
        print("Loyalty: Customer created successfully.")
    else:
        print("FAILED: Customer creation.")
        
    # 2. Test Points Accrual
    prod_ctrl = ProductController()
    cat_id = prod_ctrl.get_all_categories()[0].id
    prod = prod_ctrl.add_product("LoyaltyItem", 10.00, cat_id)
    
    order_ctrl = OrderController()
    
    # Buy item worth $10 -> Expect 10 points
    try:
        # Mock product object for controller
        mock_item = {'product': prod, 'qty': 1}
        # Direct DB object for order creation to avoid session detach issues in test
        db = SessionLocal()
        prod_db = db.query(prod.__class__).get(prod.id)
        prod_db.stock_quantity = 100 # Ensure stock
        db.commit()
        db.close()
        
        order_ctrl.create_order([mock_item], 10.00, customer_id=cust.id)
        
        # Verify points
        db = SessionLocal()
        updated_cust = db.query(Customer).get(cust.id)
        if updated_cust.points == 10:
             print("Loyalty: Points added correctly (0 -> 10).")
        else:
             print(f"FAILED: Points mismatch. Expected 10, got {updated_cust.points}")
        db.close()
        
    except Exception as e:
        print(f"FAILED: Order/Loyalty flow: {e}")

    print("PHASE 4 VERIFICATION COMPLETE")

if __name__ == "__main__":
    verify_phase_4()
