from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas, crud
from ..database import get_db
from typing import List
import typing as t

router = APIRouter()

OBJECTS_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/objects"
NODES_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/nodes"
QUEUE_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/queue"
RESULT_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/video_results"

@router.get("/", response_model=t.List[schemas.ObjectReturn])
async def get_all_objects_endpoint(
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth2.require_user)
    ):
    objects = await crud.get_objects(db)
    return objects


@router.get("/myObjects", response_model=t.List[schemas.ObjectReturn])
async def get_only_my_objects_endpoint(
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth2.require_user)
    ):
    objects = await crud.get_only_my_objects(db, user_id=current_user.user_id)
    return objects

@router.get("/userObjects", response_model=t.List[schemas.ObjectReturn])
async def get_only_user_objects_endpoint(
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth2.require_user)
    ):
    objects = await crud.get_only_user_objects(db)
    return objects

@router.get("/{id}", response_model=schemas.ObjectReturn, status_code=status.HTTP_201_CREATED)
async def get_object_by_id_endpoint(
    id: int,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    object = await crud.get_object_by_id(db, id)
    return object


@router.put("/{id}", response_model=schemas.ObjectReturn, status_code=status.HTTP_201_CREATED)
async def update_object_endpoint(
    object_id: int, 
    object: schemas.ObjectUpdate, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth2.require_user)
    ):
    object = await crud.object_update(db, object_id, current_user.user_id, object)
    return object