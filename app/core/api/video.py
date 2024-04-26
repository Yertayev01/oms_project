from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas, crud
from ..database import get_db
from typing import List
import typing as t
from fastapi.responses import JSONResponse
import base64

router = APIRouter()

OBJECTS_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/objects"
NODES_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/nodes"
QUEUE_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/queue"
RESULT_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/video_results"

@router.get("/myVideos", response_model=t.List[schemas.VideoReturn])
async def get_only_my_videos_endpoint(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    videos = await crud.get_only_my_videos(db, user_id=current_user.user_id)
    return videos

@router.get("/userVideos", response_model=t.List[schemas.VideoReturn])
async def get_only_user_videos_endpoint(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    videos = await crud.get_only_my_videos(db)
    return videos