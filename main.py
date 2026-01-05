import sys
from PyQt6.QtWidgets import QApplication
from ui.styles import DARK_THEME_QSS
from ui.main_window import MainWindow
from ui.login_window import LoginWindow
from data.database import init_db

def main():
    init_db()
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME_QSS)
    
    # Store references to keep windows alive
    login_window = LoginWindow()
    main_window = None

    def show_main_window(role):
        nonlocal main_window
        main_window = MainWindow(role)
        main_window.show()

    login_window.login_successful.connect(show_main_window)
    login_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
