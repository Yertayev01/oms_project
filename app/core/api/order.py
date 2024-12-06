from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import crud, schemas, database, oauth2, models
from typing import List

router = APIRouter()


@router.post("/orders", response_model=schemas.OrderReturn)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db), current_user: schemas.UserReturn = Depends(oauth2.require_user)):
    return crud.place_order(db, current_user.id, order)

@router.get("/orders", response_model=List[schemas.OrderReturn])
async def get_user_orders(
    db: Session = Depends(database.get_db), 
    current_user: schemas.UserReturn = Depends(oauth2.require_user),
    status: str = None, 
    start_date: str = None, 
    end_date: str = None,
    limit: int = 10,
    offset: int = 0
):
    # Paginate and filter orders based on status and date range
    orders = crud.get_user_orders(db, current_user.id, status, start_date, end_date)
    
    # Apply pagination
    orders = orders[offset: offset + limit]
    
    return orders

@router.get("/orders/{order_id}", response_model=schemas.OrderReturn)
async def get_order(order_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserReturn = Depends(oauth2.require_user)):
    return crud.get_order_by_id(db, order_id, current_user.id)

@router.patch("/orders/{order_id}", response_model=schemas.OrderReturn)
async def cancel_order(order_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserReturn = Depends(oauth2.require_user)):
    return crud.cancel_order(db, order_id, current_user.id)


@router.get("/admin/orders", response_model=List[schemas.OrderReturn])
async def admin_get_orders(db: Session = Depends(database.get_db)):
    return db.query(models.Order).all()

@router.patch("/admin/orders/{order_id}", response_model=schemas.OrderReturn)
async def admin_update_order_status(order_id: int, status: schemas.OrderStatus, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    order.status = status
    db.commit()
    db.refresh(order)
    return order
