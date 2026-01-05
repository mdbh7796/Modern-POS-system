from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QPushButton, QHBoxLayout, QLabel, QLineEdit, 
                             QComboBox, QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from controllers.product_controller import ProductController
from controllers.order_controller import OrderController

from ui.reports_widget import ReportsWidget

class AdminWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Admin Dashboard")
        self.resize(800, 600)
        
        # Controllers
        self.product_ctrl = ProductController()
        self.order_ctrl = OrderController()
        
        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # 1. Sales History Tab
        self.history_tab = QWidget()
        self.init_history_tab()
        self.tabs.addTab(self.history_tab, "Sales History")
        
        # 2. Product Management Tab
        self.products_tab = QWidget()
        self.init_products_tab()
        self.tabs.addTab(self.products_tab, "Products")
        
        # 3. Reports Tab
        self.reports_widget = ReportsWidget()
        self.tabs.addTab(self.reports_widget, "Reports")
        self.tabs.currentChanged.connect(self.on_tab_change)

    def on_tab_change(self, index):
        if self.tabs.tabText(index) == "Reports":
            self.reports_widget.refresh_chart()

    def init_history_tab(self):
        layout = QVBoxLayout(self.history_tab)
        
        # Refresh Button
        refresh_btn = QPushButton("Refresh History")
        refresh_btn.clicked.connect(self.load_history)
        layout.addWidget(refresh_btn)
        
        # Table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Order ID", "Date", "Total", "Status"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.history_table)
        
        self.load_history()

    def load_history(self):
        orders = self.order_ctrl.get_order_history()
        self.history_table.setRowCount(0)
        
        for order in orders:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            
            self.history_table.setItem(row, 0, QTableWidgetItem(str(order.id)))
            self.history_table.setItem(row, 1, QTableWidgetItem(order.timestamp.strftime("%Y-%m-%d %H:%M")))
            self.history_table.setItem(row, 2, QTableWidgetItem(f"${order.total_amount:.2f}"))
            self.history_table.setItem(row, 3, QTableWidgetItem(order.status.value))

    def init_products_tab(self):
        layout = QHBoxLayout(self.products_tab)
        
        # Left: Product List
        left_panel = QVBoxLayout()
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(3)
        self.product_table.setHorizontalHeaderLabels(["ID", "Name", "Price"])
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.product_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.product_table.itemClicked.connect(self.on_product_selected)
        
        left_panel.addWidget(QLabel("Existing Products"))
        left_panel.addWidget(self.product_table)
        
        refresh_btn = QPushButton("Refresh Products")
        refresh_btn.clicked.connect(self.load_products)
        left_panel.addWidget(refresh_btn)
        
        layout.addLayout(left_panel, stretch=2)
        
        # Right: Add/Edit Form
        right_panel = QVBoxLayout()
        right_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        form_title = QLabel("Add New Product")
        form_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        right_panel.addWidget(form_title)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Product Name")
        right_panel.addWidget(self.name_input)
        
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price (e.g. 3.50)")
        right_panel.addWidget(self.price_input)
        
        self.category_combo = QComboBox()
        self.load_categories_into_combo()
        right_panel.addWidget(self.category_combo)
        
        add_btn = QPushButton("Add Product")
        add_btn.clicked.connect(self.add_product)
        right_panel.addWidget(add_btn)
        
        delete_btn = QPushButton("Delete Selected")
        delete_btn.setObjectName("SecondaryButton")
        delete_btn.clicked.connect(self.delete_product)
        right_panel.addWidget(delete_btn)
        
        layout.addLayout(right_panel, stretch=1)
        
        self.load_products()

    def load_categories_into_combo(self):
        self.category_combo.clear()
        categories = self.product_ctrl.get_all_categories()
        for cat in categories:
            self.category_combo.addItem(cat.name, userData=cat.id)

    def load_products(self):
        # Flattened list for simplicity
        products = []
        categories = self.product_ctrl.get_all_categories()
        for cat in categories:
            products.extend(self.product_ctrl.get_products_by_category(cat.id))
            
        self.product_table.setRowCount(0)
        for p in products:
            row = self.product_table.rowCount()
            self.product_table.insertRow(row)
            self.product_table.setItem(row, 0, QTableWidgetItem(str(p.id)))
            self.product_table.setItem(row, 1, QTableWidgetItem(p.name))
            self.product_table.setItem(row, 2, QTableWidgetItem(f"${p.price:.2f}"))

    def add_product(self):
        name = self.name_input.text().strip()
        price_text = self.price_input.text().strip()
        category_id = self.category_combo.currentData()
        
        if not name or not price_text:
            QMessageBox.warning(self, "Invalid Input", "Please fill in all fields")
            return
            
        try:
            price = float(price_text)
            self.product_ctrl.add_product(name, price, category_id)
            self.load_products()
            self.name_input.clear()
            self.price_input.clear()
            QMessageBox.information(self, "Success", "Product added successfully")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Price must be a number")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_product_selected(self, item):
        pass # Placeholder for edit functionality

    def delete_product(self):
        rows = self.product_table.selectionModel().selectedRows()
        if not rows:
            return
            
        row = rows[0].row()
        product_id = int(self.product_table.item(row, 0).text())
        
        confirm = QMessageBox.question(self, "Confirm Delete", 
                                     "Are you sure you want to delete this product?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            if self.product_ctrl.delete_product(product_id):
                self.load_products()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete product")

    def closeEvent(self, event):
        self.product_ctrl.close()
        self.order_ctrl.close()
        event.accept()
