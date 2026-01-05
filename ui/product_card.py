from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QColor

class ProductCard(QFrame):
    clicked = pyqtSignal(int)  # Signal emitting product ID

    def __init__(self, product_id, name, price, image_url=None):
        super().__init__()
        self.product_id = product_id
        self.setObjectName("ProductCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedWidth(180)
        self.setFixedHeight(180) # Fixed size for grid consistence

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Placeholder Image (In a real app, load from URL or path)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #444; border-radius: 8px;")
        self.image_label.setFixedHeight(100)
        
        # Display initials or icon if no image
        self.image_label.setText(name[:2].upper()) 
        self.image_label.setStyleSheet("background-color: #444; border-radius: 8px; font-size: 30px; color: #888;")
        
        layout.addWidget(self.image_label)

        # Product Name
        self.name_label = QLabel(name)
        self.name_label.setObjectName("ProductName")
        self.name_label.setWordWrap(True)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label)

        # Price and Stock
        self.price_label = QLabel(f"${price:.2f}")
        self.price_label.setObjectName("ProductPrice")
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.price_label)

    def update_stock_display(self, stock):
         # Could be used to visually grey out if stock is 0
         if stock <= 0:
             self.setEnabled(False)
             self.name_label.setText(f"{self.name_label.text()} (Out of Stock)")
         else:
             self.setEnabled(True)

    def update_price_display(self, formatted_price):
        self.price_label.setText(formatted_price)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.product_id)
            # Add a small visual feedback eventually?
        super().mousePressEvent(event)
