from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas, crud, database
from ..database import get_db
import typing as t
from typing import List
from fastapi.responses import JSONResponse
router = APIRouter()

@router.post("/userProfile", response_model=schemas.UserProfileReturn)
async def userProfile(
    db: Session = Depends(database.get_db),
    current_user: str = Depends(oauth2.require_user)
):
    userProfile = await crud.get_user_profile(db, id)

    if not userProfile:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"})

    return userProfile

@router.post("/myProfile", response_model=schemas.UserProfileReturn)
async def userProfile(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.require_user)
):
    userProfile = await crud.get_my_profile(db, user_id=current_user.user_id)

    if not userProfile:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"})

    return userProfile

@router.post("/follow", response_model=schemas.FollowReturn, status_code=status.HTTP_202_ACCEPTED)
async def follow(
    db: Session = Depends(database.get_db),
    current_user: str = Depends(oauth2.require_user)
    ):
    
    follow = await crud.follow_user(db, schemas.FollowUser(user_id=current_user.user_id))
    db.refresh(follow)

    return follow

@router.get("/followerList", response_model=t.List[schemas.FollowList])
async def follows(
    db: Session = Depends(database.get_db),
    current_user: str = Depends(oauth2.require_user)
):
    follows = await crud.get_follow_list(db)
    return follows