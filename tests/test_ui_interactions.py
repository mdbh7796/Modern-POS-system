import pytest
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from data.models import Product

def test_main_window_initialization(qtbot):
    """Test that MainWindow initializes with the correct title."""
    window = MainWindow(role="cashier")
    qtbot.addWidget(window)
    assert "Coffee Shop POS - Cashier" in window.windowTitle()

def test_add_to_cart(qtbot, db_session):
    """Test adding a product to the cart."""
    window = MainWindow(role="cashier")
    qtbot.addWidget(window)
    
    # Get a product from the DB (seeded by init_db in conftest)
    product = db_session.query(Product).first()
    if not product:
        pytest.skip("No product data available in DB for testing")
        
    # Manually trigger add to cart
    window.add_to_cart_by_id(product.id)
    
    assert len(window.cart_items) == 1
    assert window.cart_items[0]['product'].id == product.id
    assert window.cart_items[0]['qty'] == 1
    
    # Check UI update (cart_list should have one item)
    assert window.cart_list.count() == 1

def test_currency_change_updates_ui(qtbot, db_session):
    """Test that changing currency updates the total label."""
    window = MainWindow(role="cashier")
    qtbot.addWidget(window)
    
    product = db_session.query(Product).first()
    if not product:
        pytest.skip("No product data available in DB for testing")
        
    window.add_to_cart_by_id(product.id)
    
    # Switch to MAD (rate 10.0)
    window.currency_combo.setCurrentText("MAD")
    
    expected_total = product.price * 10.0
    assert f"{expected_total:.2f} DH" in window.total_label.text()

def test_receipt_currency_formatting(qtbot, db_session, tmp_path):
    """Test that the generated receipt uses the selected currency symbol."""
    from services.receipt_service import ReceiptService
    import os
    
    # Use a temporary directory for receipts in this test
    receipt_dir = tmp_path / "receipts"
    receipt_dir.mkdir()
    
    window = MainWindow(role="cashier")
    window.receipt_service = ReceiptService(output_dir=str(receipt_dir))
    qtbot.addWidget(window)
    
    product = db_session.query(Product).first()
    window.add_to_cart_by_id(product.id)
    
    # Switch to EUR
    window.currency_combo.setCurrentText("EUR")
    
    # Process order
    window.process_order(product.price)
    
    # Find the receipt file
    files = os.listdir(receipt_dir)
    assert len(files) == 1
    
    with open(receipt_dir / files[0], "r", encoding="utf-8") as f:
        content = f.read()
        # EUR symbol is €
        assert "€" in content
        # Check if the converted price is present (simplified check)
        eur_price = product.price * 0.95
        assert f"{eur_price:.2f}" in content
