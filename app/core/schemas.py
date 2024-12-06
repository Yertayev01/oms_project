from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional, List
from datetime import datetime
import typing as t
from .models import Order

# Token schema
class Token(BaseModel):
    id: int
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

# User schemas
class UserBase(BaseModel):
    name: str
    is_admin: t.Optional[bool] = False

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_admin: t.Optional[bool] = False

class UserAdminCreate(BaseModel):
    name: str
    password: str
    is_admin: t.Optional[bool] = False

class UserReturn(BaseModel):
    id: int
    email: str
    name: str
    is_admin: bool

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    name: str
    password: t.Optional[str] = None

class UserAdminUpdate(UserBase):
    name: str
    is_admin: t.Optional[bool] = False
    password: t.Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

# Order schemas
class OrderStatus(Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    canceled = "canceled"

# Order schemas
class OrderBase(BaseModel):
    total_price: float
    status: OrderStatus  # Use the Enum directly

# OrderItem schemas
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

    
class OrderCreate(OrderBase):
    user_id: int
    status: OrderStatus = OrderStatus.pending
    items: List['OrderItemCreate']

class OrderResponse(BaseModel):
    order_id: int
    status: OrderStatus  # This should be a string serialized version of the Enum

class OrderReturn(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: OrderStatus  # This will be serialized as a string, since OrderStatus is a subclass of str
    created_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True

from pydantic import root_validator

class OrderReturn(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: OrderStatus
    created_at: datetime

    class Config:
        orm_mode = True

    @root_validator(pre=True)
    def enum_to_str(values):
        if isinstance(values, dict):
            if 'status' in values and isinstance(values['status'], Enum):
                return values['status'].value  # Or any other processing
        elif isinstance(values, Order):
            if isinstance(values.status, Enum):
                return values.status.value  # Convert Enum to string
        return values  # Return values as is if no match


# Product schemas
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductReturn(ProductBase):
    id: int

    class Config:
        orm_mode = True

# Promotion schemas
class PromotionBase(BaseModel):
    name: str
    discount_type: str  # 'percentage' or 'fixed'
    value: float
    start_date: datetime
    end_date: datetime
    applicable_products: t.List[int]  # List of product ids

class PromotionCreate(PromotionBase):
    pass

class PromotionReturn(PromotionBase):
    id: int

    class Config:
        orm_mode = True

# ProductPromotion schemas
class ProductPromotionCreate(BaseModel):
    product_id: int
    promotion_id: int

class ProductPromotionReturn(BaseModel):
    product_id: int
    promotion_id: int

    class Config:
        orm_mode = True
