from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import crud, schemas, database, oauth2, models
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/promotions", response_model=schemas.PromotionReturn)
async def create_promotion(promotion: schemas.PromotionCreate, db: Session = Depends(database.get_db)):
    return crud.create_promotion(db, promotion)

@router.patch("/promotions/{promotion_id}", response_model=schemas.PromotionReturn)
async def update_promotion(promotion_id: int, promotion: schemas.PromotionCreate, db: Session = Depends(database.get_db)):
    return crud.update_promotion(db, promotion_id, promotion)

@router.get("/promotions", response_model=List[schemas.PromotionReturn])
async def get_promotions(db: Session = Depends(database.get_db)):
    # Get active promotions based on date range
    promotions = db.query(models.Promotion).filter(
        models.Promotion.start_date <= datetime.utcnow(), 
        models.Promotion.end_date >= datetime.utcnow()
    ).all()
    return promotions