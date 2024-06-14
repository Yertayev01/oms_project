from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas, crud
from ..database import get_db
from typing import List
import typing as t
from fastapi.responses import JSONResponse
import base64
import time
from ..config import settings

router = APIRouter()

# Rate limiter configuration
RATE_LIMIT = 10  # Number of allowed requests
TIME_WINDOW = 60  # Time window in seconds

# In-memory store for rate limiting (use Redis or similar for production)
request_times = {}

def rate_limiter(USER_ID: int):
    current_time = time.time()

    # Initialize user's request times if not present
    if USER_ID not in request_times:
        request_times[USER_ID] = []

    # Filter out requests outside the time window
    request_times[USER_ID] = [timestamp for timestamp in request_times[USER_ID] if current_time - timestamp < TIME_WINDOW]

    # Check if the number of requests is within the limit
    if len(request_times[USER_ID]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests, please try again later.")

    # Add the current request timestamp
    request_times[USER_ID].append(current_time)




@router.get("/", response_model=t.List[schemas.ObjectsReturn])
async def get_all_objects_endpoint(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    rate_limiter(current_user.USER_MNG_ID)
    objects = await crud.get_objects(db)
    return objects

@router.get("/myAssets", response_model=t.List[schemas.ObjectsReturn])
async def get_only_my_objects_endpoint(
    asset_type: str,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
):
    rate_limiter(current_user.USER_MNG_ID)
    assets = await crud.get_only_my_objects(db, user_id=current_user.USER_MNG_ID, asset_type=asset_type)
    return assets

@router.get("/userAssets", response_model=t.List[schemas.ObjectsReturn])
async def get_only_user_objects_endpoint(
    asset_type: str,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
):
    rate_limiter(current_user.USER_MNG_ID)
    assets = await crud.get_only_user_objects(db, user_id=current_user.USER_MNG_ID, asset_type=asset_type)
    return assets

import os
import logging
logging.basicConfig(level=logging.DEBUG)

@router.get("/{id}", response_model=schemas.AssetReturn, status_code=status.HTTP_200_OK)
async def get_asset_by_id_endpoint(
    id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.require_user)
):
    rate_limiter(current_user.USER_MNG_ID)
    asset = await crud.get_asset_by_id(db, id)
    
    if not asset:
        logging.debug(f"Asset with ID {id} not found")
        raise HTTPException(status_code=404, detail="Asset not found")

    nerf_file_path, chng_file_nm = asset

    file_path = f"{settings.objects_folder}/{nerf_file_path}/{chng_file_nm}"
    logging.debug(f"Constructed file path: {file_path}")

    if not os.path.exists(file_path):
        logging.debug(f"File at path {file_path} not found")
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
            logging.debug(f"File content read successfully, size: {len(file_content)} bytes")
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        raise HTTPException(status_code=500, detail="Error reading file")

    return schemas.AssetReturn(json_file=file_content)



@router.put("/{id}", response_model=schemas.AssetReturn, status_code=status.HTTP_201_CREATED)
async def update_object_endpoint(
    id: str, 
    asset: schemas.AssetUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    rate_limiter(current_user.USER_MNG_ID)
    asset = await crud.object_update(db, id, current_user.USER_MNG_ID, asset)
    return asset