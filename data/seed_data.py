from data.database import init_db, SessionLocal
from data.models import Category, Product, User

def seed_data():
    init_db()
    db = SessionLocal()

    if db.query(Category).first():
        print("Database already seeded. Checking for updates...")
        # Check if users exist (migration support)
        if not db.query(User).first():
            print("Seeding users...")
            admin = User(username="admin", password_hash="admin123", role="admin")
            cashier = User(username="cashier", password_hash="cashier123", role="cashier")
            db.add_all([admin, cashier])
            db.commit()
        return

    # Categories
    cat_coffee = Category(name="Coffee")
    cat_pastry = Category(name="Pastry")
    cat_tea = Category(name="Tea")

    db.add_all([cat_coffee, cat_pastry, cat_tea])
    db.commit()

    # Products with Stock
    products = [
        Product(name="Espresso", price=3.00, category=cat_coffee, image_url="espresso.png", stock_quantity=100),
        Product(name="Latte", price=4.50, category=cat_coffee, image_url="latte.png", stock_quantity=50),
        Product(name="Cappuccino", price=4.00, category=cat_coffee, image_url="cappuccino.png", stock_quantity=50),
        Product(name="Croissant", price=3.50, category=cat_pastry, image_url="croissant.png", stock_quantity=20),
        Product(name="Muffin", price=2.50, category=cat_pastry, image_url="muffin.png", stock_quantity=30),
        Product(name="Green Tea", price=3.00, category=cat_tea, image_url="green_tea.png", stock_quantity=40),
        Product(name="Cake Slice", price=5.00, category=cat_pastry, image_url="cake.png", stock_quantity=10),
    ]

    db.add_all(products)
    
    # Users
    admin = User(username="admin", password_hash="admin123", role="admin")
    cashier = User(username="cashier", password_hash="cashier123", role="cashier")
    db.add_all([admin, cashier])

    db.commit()
    print("Database seeded successfully.")
    db.close()

if __name__ == "__main__":
    seed_data()
