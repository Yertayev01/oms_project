from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas, crud
from ..database import get_db
from typing import List
import typing as t
from fastapi.responses import JSONResponse
import base64

router = APIRouter()


@router.get("/", response_model=t.List[schemas.ObjectReturn])
async def get_all_objects_endpoint(
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth2.require_user)
    ):
    objects = await crud.get_objects(db)
    return objects


@router.get("/myObjects", response_model=t.List[schemas.ObjectsReturn])
async def get_only_my_objects_endpoint(
    object_type: str,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    objects = await crud.get_only_my_objects(db, user_id=current_user.user_id, object_type=object_type)
    return objects

@router.get("/userObjects", response_model=t.List[schemas.ObjectsReturn])
async def get_only_user_objects_endpoint(
    object_type: str,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
):
    objects = await crud.get_only_user_objects(db, object_type=object_type, user_id=current_user.user_id)
    return objects

@router.get("/{id}", response_model=schemas.ObjectReturn, status_code=status.HTTP_201_CREATED)
async def get_object_by_id_endpoint(
    id: int,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    object = await crud.get_object_by_id(db, id)
    if not object:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Object not found"})
    
    json_url = f"C:/Users/USER/Desktop/anchorWorld_auth/objects/{object.object_file_path}/{object.object_file_name}"

    with open(json_url, "rb") as file:
        json_file = base64.b64encode(file.read()).decode()

    # Convert node to dictionary and add the json_url
    object_dict = object.__dict__
    object_dict['json_file'] = json_file

    # Remove the sqlalchemy internal attributes
    object_dict.pop('_sa_instance_state', None)
    
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