# Modern-POS-system
A professional, dark-themed Shop POS system built with Python and PyQt6. Features real-time inventory management, customer loyalty tracking, multi-currency support, and Matplotlib sales analytics.

Shop POS System
A high-performance, dark-themed desktop Point of Sale (POS) application built with Python and PyQt6. This project implements a full retail workflow, from user authentication and product management to real-time sales reporting and customer loyalty tracking.

🚀 Key Features
1. Intuitive Sales Interface
Dynamic Product Catalog: Products are organized into tabs (e.g., Coffee, Pastry, Tea) and displayed as high-quality visual cards.

Real-time Cart Management: Seamlessly add items to a cart, adjust quantities, and view live total calculations.

Multi-Currency Support: Integrated CurrencyService allows users to switch between USD, EUR, and MAD with automatic price conversion.

2. Administration & Inventory
Secure Authentication: Role-based access control (Admin vs. Cashier) ensures sensitive features like reporting are protected.

Product Management: Full CRUD (Create, Read, Delete) capabilities for the product catalog directly through the Admin Dashboard.

Stock Tracking: Automatically monitors inventory levels and visually flags "Out of Stock" items to prevent overselling.

3. Customer Loyalty & Receipts
Loyalty Program: Track customer purchases and award points automatically based on transaction totals (e.g., 1 point per $1 spent).

Automated Receipt Generation: Automatically generates professional text-based receipts for every transaction, saved locally for record-keeping.

4. Data & Analytics
Sales Reporting: Built-in ReportsWidget uses Matplotlib to visualize sales trends and revenue over time.

Robust Database: Powered by SQLite and SQLAlchemy for reliable data persistence and structured relationships between Products, Orders, and Customers.

Database Migrations: Implements Alembic to manage database schema changes safely.

🛠️ Tech Stack
GUI Framework: PyQt6

ORM: SQLAlchemy

Database: SQLite

Migrations: Alembic

Data Visualization: Matplotlib

Icons: QtAwesome

📂 Project Structure
ui/: Custom PyQt widgets and windows (Login, Admin, Checkout).

controllers/: Business logic handling for orders, products, and customers.

services/: Helper services for currency conversion and receipt generation.

data/: Database models, initialization scripts, and seed data.

migrations/: Alembic version history for database schema.
