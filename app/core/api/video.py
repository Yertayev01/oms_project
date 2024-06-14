from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas, crud
from ..database import get_db
from typing import List
import typing as t
from fastapi.responses import JSONResponse
import base64
from ..config import settings
import logging, os

router = APIRouter()

@router.get("/", response_model=t.List[schemas.VideoReturn])
async def get_all_videos_endpoint(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    videos = await crud.get_videos(db)

    return videos

@router.get("/myVideos", response_model=t.List[schemas.VideoReturn])
async def get_only_my_videos_endpoint(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    videos = await crud.get_only_my_videos(db, user_id=current_user.USER_MNG_ID)
    return videos

@router.get("/userVideos", response_model=t.List[schemas.VideoReturn])
async def get_only_user_videos_endpoint(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    videos = await crud.get_only_user_videos(db, user_id=current_user.USER_MNG_ID)
    return videos

@router.get("/{id}", response_model=schemas.VideoFile, status_code=status.HTTP_200_OK)
async def get_video_by_id_endpoint(
    id: str,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
):
    video = await crud.get_video_by_id(db, id)
    if not video:
        logging.debug(f"Video with ID {id} not found")
        raise HTTPException(status_code=404, detail="Video not found")
    
    video_file_path, video_file_name = video
    
    video_path = f"{settings.video_folder}/{video_file_path}/{video_file_name}"
    logging.debug(f"Constructed file path: {video_path}")

    if not os.path.exists(video_path):
        logging.debug(f"File at path {video_path} not found")
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(video_path, "rb") as file:
            file_content = file.read()
            logging.debug(f"File content read successfully, size: {len(file_content)} bytes")
            encoded_content = base64.b64encode(file_content).decode('utf-8')
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        raise HTTPException(status_code=500, detail="Error reading file")

    return schemas.VideoFile(video_file=encoded_content)

@router.put("/{id}", response_model=schemas.VideoReturn, status_code=status.HTTP_200_OK)
async def update_video_endpoint(
    id: str, 
    video: schemas.VideoUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    video = await crud.video_update(db, id, current_user.USER_MNG_ID, video)
    return video