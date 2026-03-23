import os

# Application Settings
APP_NAME = "Coffee Shop POS"
DEFAULT_WINDOW_SIZE = (1200, 800)

# Currency Settings
SUPPORTED_CURRENCIES = ["USD", "EUR", "MAD"]
DEFAULT_CURRENCY = "USD"

# Database Settings
DATABASE_URL = "sqlite:///./coffee_shop.db"

# Receipt Settings
RECEIPT_DIR = "receipts"

# Business Logic
LOYALTY_POINTS_PER_UNIT = 1.0  # 1 point per 1 unit of currency (USD)
