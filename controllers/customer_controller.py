from data.database import SessionLocal
from data.models import Customer
from sqlalchemy.exc import IntegrityError

class CustomerController:
    def __init__(self):
        self.db = SessionLocal()

    def find_customer_by_phone(self, phone):
        return self.db.query(Customer).filter(Customer.phone == phone).first()

    def create_customer(self, phone, name=None):
        try:
            new_customer = Customer(phone=phone, name=name, points=0)
            self.db.add(new_customer)
            self.db.commit()
            return new_customer
        except IntegrityError:
            self.db.rollback()
            return None # Phone already exists

    def add_points(self, customer_id, points):
        customer = self.db.query(Customer).get(customer_id)
        if customer:
            customer.points += points
            self.db.commit()
            return customer.points
        return 0
    
    def close(self):
        self.db.close()
