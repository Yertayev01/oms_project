from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas, crud
from ..database import get_db
from typing import List
import typing as t
from fastapi.responses import JSONResponse
import base64
from ..config import settings

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
    videos = await crud.get_only_my_videos(db, user_id=current_user.user_id)
    return videos

@router.get("/userVideos", response_model=t.List[schemas.VideoReturn])
async def get_only_user_videos_endpoint(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    videos = await crud.get_only_my_videos(db)
    return videos

@router.get("/{id}", response_model=schemas.VideoReturn, status_code=status.HTTP_201_CREATED)
async def get_video_by_id_endpoint(
    id: int,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
):
    video = await crud.get_video_by_id(db, id)
    if not video:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Video not found"})
    
    # Construct the URL using node_json_path and node_json_name
    #json_url = f"http://192.168.0.130:8010/api/json/{node.node_json_path}/{node.node_json_name}"
    json_url = f"{settings.video_folder}/{video.video_file_path}/{video.video_file_name}"

    with open(json_url, "rb") as file:
        json_file = base64.b64encode(file.read()).decode()

    # Convert node to dictionary and add the json_url
    video_dict = video.__dict__
    video_dict['json_file'] = json_file

    # Remove the sqlalchemy internal attributes
    video_dict.pop('_sa_instance_state', None)

    return video_dict

@router.put("/{id}", response_model=schemas.NodeReturn, status_code=status.HTTP_201_CREATED)
async def update_node_endpoint(
    id: int, 
    node: schemas.NodeUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    node = await crud.node_update(db, id, current_user.user_id, node)
    return node