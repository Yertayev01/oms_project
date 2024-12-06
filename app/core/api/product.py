from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import crud, schemas, database, oauth2, models
from typing import List

router = APIRouter()

@router.post("/products", response_model=schemas.ProductReturn)
async def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    return crud.create_product(db, product)

@router.patch("/products/{product_id}", response_model=schemas.ProductReturn)
async def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    return crud.update_product(db, product_id, product)

@router.get("/products", response_model=List[schemas.ProductReturn])
async def get_products(db: Session = Depends(database.get_db), limit: int = 10, offset: int = 0):
    # Get products with stock > 0 and apply pagination
    products = db.query(models.Product).filter(models.Product.stock > 0).all()
    
    # Apply pagination
    products = products[offset: offset + limit]
    
    return products

