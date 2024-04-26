from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas, crud
from ..database import get_db
from typing import List

router = APIRouter()


@router.get("/", response_model=List[schemas.ObjectLikeReturn])
async def get_all_object_likes(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    likes = await crud.get_object_likes(db)
    return likes

@router.get("/", response_model=List[schemas.NodeLikeReturn])
async def get_all_node_likes(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    likes = await crud.get_node_likes(db)
    return likes

@router.post("/postObjectLike", status_code=status.HTTP_201_CREATED)
async def like_object(
    like: schemas.ObjectLikeCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    created_like = await crud.post_object_like(db, like, current_user.user_id)
    return  created_like

@router.post("/postNodeLike", status_code=status.HTTP_201_CREATED)
async def like_object(
    like: schemas.NodeLikeCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    created_like = await crud.post_node_like(db, like, current_user.user_id)
    return created_like

@router.delete("/objectDelete/{comment_id}", response_model=schemas.ObjectLikeReturn, status_code=status.HTTP_202_ACCEPTED)
async def object_delete_like(
    id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    deleted_like = await crud.object_like_delete(db, id)
    return deleted_like


@router.delete("/nodeDelete/{comment_id}", response_model=schemas.NodeLikeReturn, status_code=status.HTTP_202_ACCEPTED)
async def node_delete_like(
    id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    deleted_like = await crud.node_like_delete(db, id)
    return deleted_like