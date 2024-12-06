from sqlalchemy import Column, Integer, String, BigInteger, func, Text, Numeric, Boolean, ForeignKey, Float, DateTime, Enum, JSON
from datetime import datetime
import enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OrderStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    canceled = "canceled"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    promotions = relationship("Promotion", secondary="product_promotions")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total_price = Column(Float)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Promotion(Base):
    __tablename__ = 'promotions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    discount_type = Column(Enum('percentage', 'fixed', name='discount_type_enum'))
    value = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    applicable_products = Column(JSON)
    products = relationship("Product", secondary="product_promotions")

class ProductPromotion(Base):
    __tablename__ = 'product_promotions'

    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    promotion_id = Column(Integer, ForeignKey('promotions.id'), primary_key=True)
