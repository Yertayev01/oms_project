from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas, crud
from ..database import get_db
from typing import List

router = APIRouter()


@router.get("/", response_model=List[schemas.ObjectSaveReturn])
async def get_all_object_saves(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    saves = await crud.get_object_saves(db)
    return saves

@router.get("/", response_model=List[schemas.NodeSaveReturn])
async def get_all_node_saves(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    saves = await crud.get_node_saves(db)
    return saves

@router.post("/postObjectSave", status_code=status.HTTP_201_CREATED)
async def save_object(
    save: schemas.ObjectSaveCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    created_save = await crud.post_object_save(db, save, current_user.user_id)
    return  created_save

@router.post("/postNodeSave", status_code=status.HTTP_201_CREATED)
async def save_object(
    save: schemas.NodeSaveCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    created_save = await crud.post_node_save(db, save, current_user.user_id)
    return created_save

@router.delete("/objectDelete/{comment_id}", response_model=schemas.ObjectSaveReturn, status_code=status.HTTP_202_ACCEPTED)
async def object_delete_save(
    id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    deleted_save = await crud.object_save_delete(db, id)
    return deleted_save


@router.delete("/nodeDelete/{comment_id}", response_model=schemas.NodeLikeReturn, status_code=status.HTTP_202_ACCEPTED)
async def node_delete_save(
    id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    deleted_save = await crud.node_save_delete(db, id)
    return deleted_save