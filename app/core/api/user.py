from fastapi import Depends, APIRouter, status, HTTPException
from app.core import schemas, crud, database, oauth2
import typing as t
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=schemas.UserReturn, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user: schemas.UserAdminCreate, 
    db: Session = Depends(database.get_db), 
    current_user: str = Depends(oauth2.require_admin)
    ):
    user = await crud.user_create(db, user)
    return user


@router.get("/", response_model=t.List[schemas.UserReturn])
async def get_all_users_endpoint(
    db: Session = Depends(database.get_db), 
    current_user: str = Depends(oauth2.require_admin)
    ):
    users = await crud.get_users(db)
    return users


@router.get("/{user_id}", response_model=schemas.UserReturn)
async def get_user_endpoint(
    user_id: int, db: Session = Depends(database.get_db), 
    current_user: str = Depends(oauth2.require_admin)
    ):
    _user = await crud.get_user_by_id(db, user_id)
    if not _user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return _user


@router.put("/{user_id}", response_model=schemas.UserReturn, status_code=status.HTTP_201_CREATED)
async def update_user_endpoint(
    user_id: int, user: schemas.UserUpdate, 
    db: Session = Depends(database.get_db), 
    current_user: str = Depends(oauth2.require_admin)
    ):
    user = await crud.user_update(db, user_id, user)
    return user


@router.delete("/{user_id}", response_model=schemas.UserReturn, status_code=status.HTTP_202_ACCEPTED)
async def delete_user_endpoint(
    user_id: int, db: Session = Depends(database.get_db), 
    current_user: str = Depends(oauth2.require_admin)
    ):
    _user = await crud.user_delete(db, user_id)
    return _user
