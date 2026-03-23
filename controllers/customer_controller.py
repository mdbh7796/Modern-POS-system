from data.database import SessionLocal

class CustomerController:
    def __init__(self):
        self.db = SessionLocal()

    def close(self):
        self.db.close()
