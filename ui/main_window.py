import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QScrollArea, QGridLayout, QLabel, QPushButton, 
                             QListWidget, QListWidgetItem, QMessageBox, QTabWidget, QComboBox)
from PyQt6.QtCore import Qt, pyqtSlot
from controllers.product_controller import ProductController
from controllers.order_controller import OrderController
from ui.product_card import ProductCard
from ui.checkout_dialog import CheckoutDialog
from ui.admin_window import AdminWindow
from services.receipt_service import ReceiptService
from services.currency_service import CurrencyService
import qtawesome as qta
from PyQt6 import QtCore

class MainWindow(QMainWindow):
    def __init__(self, role="cashier"):
        super().__init__()
        self.role = role
        self.setWindowTitle(f"Coffee Shop POS - {role.title()}")
        self.resize(1200, 800)
        
        # Controllers
        self.product_ctrl = ProductController()
        self.order_ctrl = OrderController()
        self.receipt_service = ReceiptService()
        self.currency_service = CurrencyService()
        
        self.cart_items = [] # List of dict: {'product': ProductObj, 'qty': int}
        
        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Side: Product Catalog
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header (Logo + Search + Currency)
        header_layout = QHBoxLayout()
        header_label = QLabel("Coffee Shop POS")
        header_label.setObjectName("HeaderLabel")
        header_layout.addWidget(header_label)
        
        header_layout.addStretch()
        
        # Currency Selector
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["USD", "EUR", "MAD"])
        self.currency_combo.setFixedWidth(80)
        self.currency_combo.currentTextChanged.connect(self.on_currency_changed)
        header_layout.addWidget(self.currency_combo)
        
        left_layout.addLayout(header_layout) # Replaces old addWidget(header_label) to now use layout
        
        # Categories Tabs
        self.category_tabs = QTabWidget()
        self.category_tabs.setStyleSheet("""
            QTabWidget::pane { border: none; }
            QTabBar::tab {
                background: #2d2d2d;
                color: #aaa;
                padding: 10px 20px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 5px;
            }
            QTabBar::tab:selected {
                background: #1e1e1e;
                color: #FF9F1C;
                border-bottom: 2px solid #FF9F1C;
            }
        """)
        self.category_tabs.currentChanged.connect(self.load_products_for_tab)
        left_layout.addWidget(self.category_tabs)

        # Product Grid Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(20)
        # Align top-left
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        self.scroll_area.setWidget(self.grid_container)
        left_layout.addWidget(self.scroll_area)

        main_layout.addWidget(left_panel, stretch=2)

        # Right Side: Cart
        self.cart_widget = QWidget()
        self.cart_widget.setObjectName("CartWidget")
        self.cart_widget.setFixedWidth(400)
        cart_layout = QVBoxLayout(self.cart_widget)
        cart_layout.setContentsMargins(20, 20, 20, 20)
        
        cart_header = QLabel("Current Order")
        cart_header.setObjectName("CartHeader")
        cart_layout.addWidget(cart_header)

        self.cart_list = QListWidget()
        cart_layout.addWidget(self.cart_list)

        # Totals
        self.total_label = QLabel("Total: $0.00")
        self.total_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FF9F1C; margin-top: 10px;")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        cart_layout.addWidget(self.total_label)

        # Checkout Button
        self.checkout_btn = QPushButton("Checkout")
        self.checkout_btn.clicked.connect(self.open_checkout)
        cart_layout.addWidget(self.checkout_btn)

        # Admin Button
        if self.role == "admin":
            self.admin_btn = QPushButton("Admin Dashboard")
            self.admin_btn.setObjectName("SecondaryButton")
            self.admin_btn.clicked.connect(self.open_admin)
            cart_layout.addWidget(self.admin_btn)

        main_layout.addWidget(self.cart_widget)

        # Initialize Data
        self.load_categories()

    def load_categories(self):
        categories = self.product_ctrl.get_all_categories()
        for cat in categories:
            self.category_tabs.addTab(QWidget(), cat.name)
        
        if categories:
            self.load_products(categories[0].id)

    def load_products_for_tab(self, index):
        cat_name = self.category_tabs.tabText(index)
        # Optimization: Store category IDs in tabs or lookup. 
        # For now, simplistic lookup from DB for simplicity of refactor.
        # Ideally, we should fetch cat ID from the tab data.
        categories = self.product_ctrl.get_all_categories()
        for cat in categories:
            if cat.name == cat_name:
                self.load_products(cat.id)
                break

    def load_products(self, category_id):
        # Clear existing items
        for i in reversed(range(self.grid_layout.count())): 
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        products = self.product_ctrl.get_products_by_category(category_id)
        
        row = 0
        col = 0
        max_cols = 3 

        for product in products:
            card = ProductCard(product.id, product.name, product.price, product.image_url)
            
            # Formatted Price Update
            fmt_price = self.currency_service.format(product.price)
            card.update_price_display(fmt_price)

            # Simple visual check
            if product.stock_quantity <= 0:
                card.setEnabled(False)
                card.name_label.setText(f"{product.name} (Out of Stock)")
            
            card.clicked.connect(self.add_to_cart_by_id)
            self.grid_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def on_currency_changed(self, currency_code):
        self.currency_service.set_currency(currency_code)
        # Reload current tab to refresh prices
        self.load_products_for_tab(self.category_tabs.currentIndex())
        self.update_cart_ui()

    @pyqtSlot(int)
    def add_to_cart_by_id(self, product_id):
        product = self.product_ctrl.get_product_by_id(product_id)
        if not product:
            return
            
        # Check if already in cart
        found = False
        for item in self.cart_items:
            if item['product'].id == product.id:
                item['qty'] += 1
                found = True
                break
        
        if not found:
            self.cart_items.append({'product': product, 'qty': 1})
            
        self.update_cart_ui()

    def open_admin(self):
        self.admin_window = AdminWindow(self)
        self.admin_window.show()

    def update_cart_ui(self):
        self.cart_list.clear()
        total_usd = 0.0
        
        for item in self.cart_items:
            product = item['product']
            qty = item['qty']
            subtotal_usd = product.price * qty
            total_usd += subtotal_usd
            
            # Formatted Item
            fmt_subtotal = self.currency_service.format(subtotal_usd)
            item_text = f"{product.name} x{qty} - {fmt_subtotal}"
            list_item = QListWidgetItem(item_text)
            self.cart_list.addItem(list_item)
            
        fmt_total = self.currency_service.format(total_usd)
        self.total_label.setText(f"Total: {fmt_total}")

    def open_checkout(self):
        if not self.cart_items:
            QMessageBox.warning(self, "Empty Cart", "Please add items to the cart first.")
            return

        total = sum(item['product'].price * item['qty'] for item in self.cart_items)
        
        # We pass the formatted string to the dialog's label manually or update dialog logic
        dialog = CheckoutDialog(total, self)
        
        # Direct UI update for Phase 5 quick win (better would be to refactor Dialog props)
        fmt_total = self.currency_service.format(total)
        dialog.total_label.setText(f"Total to Pay: {fmt_total}")
        
        if dialog.exec():
            # Pass customer_id from dialog
            self.process_order(total, dialog.customer_id)

    def process_order(self, total_amount, customer_id=None):
        try:
            new_order = self.order_ctrl.create_order(self.cart_items, total_amount, customer_id)
            
            # Generate Receipt
            receipt_path = self.receipt_service.generate_receipt(new_order, self.cart_items)
            
            # Reset UI
            self.cart_items = []
            self.update_cart_ui()
            QMessageBox.information(self, "Success", f"Order placed successfully!\nReceipt saved to: {receipt_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save order: {e}")

    def closeEvent(self, event):
        self.product_ctrl.close()
        self.order_ctrl.close()
        event.accept()
