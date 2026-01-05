
# Premium Dark Theme for Coffee Shop POS

DARK_THEME_QSS = """
/* Global */
QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}

/* Product Card */
QFrame#ProductCard {
    background-color: #2d2d2d;
    border-radius: 12px;
    border: 1px solid #3d3d3d;
}

QFrame#ProductCard:hover {
    background-color: #3d3d3d;
    border: 1px solid #FF9F1C;
}

QLabel#ProductName {
    font-weight: bold;
    font-size: 16px;
    color: #ffffff;
    background-color: transparent;
}

QLabel#ProductPrice {
    color: #FF9F1C;
    font-weight: bold;
    font-size: 15px;
    background-color: transparent;
}

/* Cart & Sidebar */
QWidget#CartWidget {
    background-color: #252526;
    border-left: 1px solid #333333;
}

QLabel#CartHeader {
    font-size: 20px;
    font-weight: bold;
    color: #FF9F1C;
    padding: 10px;
    background-color: transparent;
}

QListWidget {
    background-color: #2d2d2d;
    border: none;
    border-radius: 8px;
    padding: 5px;
    outline: none;
}

QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid #3d3d3d;
    color: #eeeeee;
}

QListWidget::item:selected {
    background-color: #3d3d3d;
    color: #FF9F1C;
    border-radius: 4px;
}

/* Buttons */
QPushButton {
    background-color: #FF9F1C;
    color: #1e1e1e;
    border: none;
    border-radius: 6px;
    padding: 12px;
    font-weight: bold;
    font-size: 15px;
}

QPushButton:hover {
    background-color: #ffb042;
}

QPushButton:pressed {
    background-color: #e58e19;
}

QPushButton#SecondaryButton {
    background-color: #3d3d3d;
    color: #cccccc;
     border: 1px solid #555555;
}

QPushButton#SecondaryButton:hover {
    background-color: #4d4d4d;
    color: #ffffff;
}

/* ScrollBar */
QScrollBar:vertical {
    border: none;
    background: #1e1e1e;
    width: 10px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: #444;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Dialogs */
QDialog {
    background-color: #1e1e1e;
}
QLabel#DialogTitle {
    font-size: 24px;
    font-weight: bold;
    color: #FF9F1C;
    margin-bottom: 15px;
}
"""
