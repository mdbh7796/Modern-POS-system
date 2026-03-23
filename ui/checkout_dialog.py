from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

class CheckoutDialog(QDialog):
    def __init__(self, total_amount, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Checkout")
        self.setModal(True)
        self.setFixedSize(400, 350)
        self.total_amount = total_amount
        self.payment_method = "Cash"
        
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

        self.setStyleSheet(self.styleSheet())
