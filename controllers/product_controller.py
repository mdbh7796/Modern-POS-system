from data.database import SessionLocal
from data.models import Product, Category
from utils.decorators import require_admin

class ProductController:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_categories(self):
        return self.db.query(Category).all()

    def get_products_by_category(self, category_id):
        return self.db.query(Product).filter(Product.category_id == category_id).all()

    def get_product_by_id(self, product_id):
        return self.db.get(Product, product_id)

    def add_product(self, name, price, category_id, image_url=None):
        new_product = Product(
            name=name,
            price=price,
            category_id=category_id,
            image_url=image_url
        )
        self.db.add(new_product)
        self.db.commit()
        return new_product

    @require_admin
    def delete_product(self, product_id):
        product = self.get_product_by_id(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False

    def close(self):
        self.db.close()
