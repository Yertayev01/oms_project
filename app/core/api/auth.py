from fastapi import Depends, APIRouter, status, HTTPException, Response, File, UploadFile
from app.core import schemas, crud, database
import typing as t
from sqlalchemy.orm import Session
from app.core.oauth2 import AuthJWT
from datetime import datetime, timedelta
from app.core.config import settings

from app.core import utils, oauth2, models

router = APIRouter()

ACCESS_TOKEN_EXPIRES_IN = settings.access_token_expires_in
REFRESH_TOKEN_EXPIRES_IN = settings.refresh_token_expires_in




@router.post("/register", response_model=schemas.UserReturn, status_code=status.HTTP_201_CREATED)
async def register(
                    user: schemas.UserCreate,
                    #photo: UploadFile,
                    db: Session = Depends(database.get_db)
                   ):
    
    # path = await utils.save_photo(photo)
    # await crud.photo_create(db, schemas.PhotoCreate(user_id=user.user_id, photo_url=path))
    
    user = await crud.user_create(db, user)
    return user


@router.post('/login')
async def login(payload: schemas.UserLogin, response: Response, Authorize: AuthJWT = Depends(), db: Session = Depends(database.get_db)):
    # Check if the user exist
    user = db.query(models.User).filter(
        models.User.username == payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Check if the password is valid
    if not await utils.verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    # Create access token
    access_token = Authorize.create_access_token(
        subject=str(user.user_id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    # Create refresh token
    refresh_token = Authorize.create_refresh_token(
        subject=str(user.user_id), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    # Store refresh and access tokens in cookie
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token, REFRESH_TOKEN_EXPIRES_IN * 60,
                        REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    # Send both access
    return {'access_token': access_token}


@router.get('/me', status_code=status.HTTP_200_OK, response_model=schemas.UserReturn)
async def me(current_user: str = Depends(oauth2.require_user)):
    return current_user


@router.get('/refresh')
async def refresh_token(response: Response, Authorize: AuthJWT = Depends(), db: Session = Depends(database.get_db)):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        user = await crud.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
        access_token = Authorize.create_access_token(
            subject=str(user.user_id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}


@router.get('/logout', status_code=status.HTTP_200_OK)
async def logout(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)
    return {'status': 'success'}
