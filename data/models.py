from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Store image path or use a placeholder if None
    # Store image path or use a placeholder if None
    image_url = Column(String, nullable=True) 
    stock_quantity = Column(Integer, default=0)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String) # For simplicity plaintext in demo, but named hash for intent
    role = Column(String) # 'admin', 'cashier'

class OrderStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    phone = Column(String, unique=True, index=True)
    points = Column(Integer, default=0)

    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    total_amount = Column(Float, default=0.0)
    status = Column(Enum(OrderStatus), default=OrderStatus.COMPLETED)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)

    items = relationship("OrderItem", back_populates="order")
    customer = relationship("Customer", back_populates="orders")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    price_at_time = Column(Float) # Store price in case product price changes later

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
