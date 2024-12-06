from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core import models, schemas, utils
from .config import settings
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core import models, schemas
from app.core.utils import calculate_total_price
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from datetime import datetime


# User-related CRUD operations

async def get_user_by_id(db: Session, id: str) -> models.User:
    return db.query(models.User).filter(models.User.id == id).first()

async def get_user_by_username(db: Session, name: str) -> models.User:
    return db.query(models.User).filter(models.User.name == name).first()

async def get_users(db: Session) -> List[models.User]:
    return db.query(models.User).all()

async def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()

async def user_create(db: Session, user: schemas.UserCreate) -> models.User:
    # Check if email exists
    existing_email = await get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(detail=f"Email {user.email} is already registered", status_code=status.HTTP_409_CONFLICT)

    # Check if username exists
    existing_username = await get_user_by_username(db, user.name)
    if existing_username:
        raise HTTPException(detail=f"Username {user.name} is already taken", status_code=status.HTTP_409_CONFLICT)
    
    # Hash password
    user.password = await utils.hash_password(user.password)
    
    # Create the user model instance
    db_user = models.User(
        **user.dict(),
    )

    # Set reg_id and mod_id to admin or some other identifier
    db_user.reg_id = settings.admin_username  # Use admin or an appropriate identifier
    db_user.mod_id = settings.admin_username  # Use admin or an appropriate identifier

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def user_update(db: Session, id: str, user: schemas.UserUpdate) -> models.User:
    db_user = await get_user_by_id(db, id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Get data for update, excluding unset values
    update_data = user.dict(exclude_unset=True)

    # Handle password update
    if "password" in update_data:
        update_data["password"] = await utils.hash_password(update_data["password"])

    # Update model fields
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def user_delete(db: Session, id: str) -> models.User:
    db_user = await get_user_by_id(db, id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return db_user

# CRUD for Order, Product, and Promotion follow similar patterns for get/create/update/delete
def place_order(db: Session, user_id: int, order_data: schemas.OrderCreate):
    # Check if all products exist and if there's enough stock
    total_price = 0.0
    items = []
    
    for item in order_data.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        if product.stock < item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough stock for product")
        
        # Calculate total price
        item_total = item.quantity * product.price
        total_price += item_total
        
        items.append(models.OrderItem(product_id=item.product_id, quantity=item.quantity))
        
        # Deduct stock (with transaction handling for concurrency)
        product.stock -= item.quantity
    
    # Commit all stock changes in a transaction
    try:
        db.add_all(items)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process order")

    # Create order with status as string
    order = models.Order(user_id=user_id, total_price=total_price, status=order_data.status, items=items)
    db.add(order)
    db.commit()
    db.refresh(order)
    
    return order

def get_user_orders(db: Session, user_id: int, status: str = None, start_date: str = None, end_date: str = None):
    query = db.query(models.Order).filter(models.Order.user_id == user_id)
    
    if status:
        query = query.filter(models.Order.status == status)
    
    if start_date and end_date:
        query = query.filter(models.Order.created_at >= start_date, models.Order.created_at <= end_date)
    
    return query.all()


def get_order_by_id(db: Session, order_id: int, user_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id, models.Order.user_id == user_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

def cancel_order(db: Session, order_id: int, user_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id, models.Order.user_id == user_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    if order.status == models.OrderStatus.SHIPPED:
        # Here, you could decide to handle it differently, for example, still cancel it but with a special condition
        order.status = models.OrderStatus.CANCELED
        db.commit()
        return order

    order.status = models.OrderStatus.CANCELED
    db.commit()
    
    return order

# Helper function to calculate the total price (considering promotions)
def calculate_total_price(db: Session, items: List[models.OrderItem]) -> float:
    total_price = 0.0
    for item in items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        price = product.price * item.quantity
        
        # Apply promotions if any
        promotions = db.query(models.Promotion).filter(
            models.Promotion.start_date <= datetime.utcnow(), 
            models.Promotion.end_date >= datetime.utcnow(),
            models.Promotion.id.in_([promo.id for promo in product.promotions])
        ).all()
        
        # Select the highest-value promotion
        max_promotion = max(promotions, key=lambda p: p.value, default=None)
        if max_promotion:
            if max_promotion.discount_type == "percentage":
                price -= price * (max_promotion.value / 100)
            elif max_promotion.discount_type == "fixed":
                price -= max_promotion.value

        total_price += price
    
    return total_price



#product
# Create a new product
def create_product(db: Session, product_data: schemas.ProductCreate) -> models.Product:
    db_product = models.Product(
        name=product_data.name,
        price=product_data.price,
        stock=product_data.stock,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Get all products with available stock
def get_products(db: Session) -> List[models.Product]:
    return db.query(models.Product).filter(models.Product.stock > 0).all()

# Update product details (e.g., price, stock)
def update_product(db: Session, product_id: int, product_data: schemas.ProductCreate) -> models.Product:
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    db_product.name = product_data.name
    db_product.price = product_data.price
    db_product.stock = product_data.stock
    db.commit()
    db.refresh(db_product)
    return db_product

