import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication)
from PyQt6.QtCore import Qt, pyqtSignal
from data.database import SessionLocal
from data.models import User

class LoginWindow(QWidget):
    login_successful = pyqtSignal(str) # Emits role on success

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coffee Shop POS - Login")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QWidget { background-color: #1e1e1e; color: #fff; font-family: 'Segoe UI'; }
            QLineEdit { padding: 10px; border: 1px solid #444; border-radius: 4px; background: #2d2d2d; color: #fff; }
            QPushButton { padding: 10px; background: #FF9F1C; color: #000; font-weight: bold; border-radius: 4px; border: none; }
            QPushButton:hover { background: #ffb042; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        title = QLabel("Welcome Back")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.attempt_login)
        layout.addWidget(self.password_input)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.attempt_login)
        layout.addWidget(login_btn)

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter fields")
            return

        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        db.close()

        # Simple plaintext check for demo
        if user and user.password_hash == password:
            self.login_successful.emit(user.role)
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    sys.exit(app.exec())
