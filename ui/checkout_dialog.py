from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QLineEdit
from PyQt6.QtCore import Qt
from controllers.customer_controller import CustomerController

class CheckoutDialog(QDialog):
    def __init__(self, total_amount, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Checkout")
        self.setModal(True)
        self.setFixedSize(400, 450)
        self.total_amount = total_amount
        self.payment_method = "Cash"
        self.customer_id = None
        
        self.cust_ctrl = CustomerController()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Title
        title = QLabel("Complete Order")
        title.setObjectName("DialogTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Total Amount
        self.total_label = QLabel(f"Total to Pay: ${self.total_amount:.2f}")
        self.total_label.setStyleSheet("font-size: 20px; color: #ffffff;")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.total_label)

        # Loyalty Section
        loyalty_label = QLabel("Customer Loyalty")
        loyalty_label.setStyleSheet("font-weight: bold; color: #FF9F1C; margin-top: 10px;")
        layout.addWidget(loyalty_label)
        
        loyalty_layout = QHBoxLayout()
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number")
        
        check_btn = QPushButton("Check")
        check_btn.setFixedWidth(60)
        check_btn.setObjectName("SecondaryButton")
        check_btn.clicked.connect(self.check_customer)
        
        loyalty_layout.addWidget(self.phone_input)
        loyalty_layout.addWidget(check_btn)
        layout.addLayout(loyalty_layout)
        
        self.loyalty_status = QLabel("")
        self.loyalty_status.setStyleSheet("color: #aaa; font-style: italic;")
        layout.addWidget(self.loyalty_status)

        # Payment Methods
        payment_layout = QHBoxLayout()
        self.cash_btn = QPushButton("Cash")
        self.cash_btn.setCheckable(True)
        self.cash_btn.setChecked(True)
        self.cash_btn.clicked.connect(lambda: self.select_payment("Cash"))
        
        self.card_btn = QPushButton("Card")
        self.card_btn.setCheckable(True)
        self.card_btn.setObjectName("SecondaryButton") 
        self.card_btn.clicked.connect(lambda: self.select_payment("Card"))

        payment_layout.addWidget(self.cash_btn)
        payment_layout.addWidget(self.card_btn)
        layout.addLayout(payment_layout)

        # Action Buttons
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("SecondaryButton")
        cancel_btn.clicked.connect(self.reject)
        
        pay_btn = QPushButton("Confirm Payment")
        pay_btn.clicked.connect(self.accept)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(pay_btn)
        layout.addLayout(btn_layout)

    def check_customer(self):
        phone = self.phone_input.text().strip()
        if not phone:
            return
            
        customer = self.cust_ctrl.find_customer_by_phone(phone)
        if customer:
            self.customer_id = customer.id
            self.loyalty_status.setText(f"Linked: {customer.name or 'Unknown'} (Points: {customer.points})")
            self.loyalty_status.setStyleSheet("color: #00ff00;")
        else:
            new_cust = self.cust_ctrl.create_customer(phone, "New Customer")
            if new_cust:
                self.customer_id = new_cust.id
                self.loyalty_status.setText(f"New Customer Created! (Points: 0)")
                self.loyalty_status.setStyleSheet("color: #FF9F1C;")
            else:
                self.loyalty_status.setText("Error linking customer.")

    def select_payment(self, method):
        self.payment_method = method
        if method == "Cash":
            self.cash_btn.setChecked(True)
            self.cash_btn.setObjectName("") 
            self.card_btn.setChecked(False)
            self.card_btn.setObjectName("SecondaryButton")
        else:
            self.card_btn.setChecked(True)
            self.card_btn.setObjectName("") 
            self.cash_btn.setChecked(False)
            self.cash_btn.setObjectName("SecondaryButton")
        
        self.setStyleSheet(self.styleSheet())
        
    def closeEvent(self, event):
        self.cust_ctrl.close()
        super().closeEvent(event)
