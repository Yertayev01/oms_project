from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, utils, database, oauth2

from datetime import datetime
from fastapi import File, UploadFile
import os
import uuid
from pydantic import ValidationError
import base64
from datetime import timedelta
from fastapi.responses import JSONResponse

router = APIRouter()

PROFILE_IMAGES_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/profile_image"
FILES_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/media_uploads"
QUEUE_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/queue"
RESULT_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/video_results"

# REGISTER USER 
@router.post("/signUp", status_code=status.HTTP_201_CREATED)#, response_model=schemas.UserReturn)
async def create_user(
    email: str,
    username: str,
    password: str,
    #firebase_token: str,
    socialKind: str,
    phone_number: int,
    latitude: str,
    longtitude: str,
    self_intro: Optional[str] = None,
    files: UploadFile = File(None),
    db: Session = Depends(database.get_db)
):
    
    upload_path = None

    if files is not None and files.filename:
        # Create a folder to save the files

        profile_image_name = os.path.basename(files.filename)

        current_date = str(datetime.now().strftime("%Y-%m-%d")) # Generate the current date as string
        
        image_uuid = uuid.uuid4().hex

        upload_path = os.path.join(PROFILE_IMAGES_FOLDER, current_date, image_uuid)
        #os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        os.makedirs(upload_path, exist_ok=True)


        pth = upload_path.replace("\\","/")
        sub_pth = pth.split("/")
        image_pth = f'{sub_pth[len(sub_pth)-2]}/{sub_pth[len(sub_pth)-1]}'
        profile_images_path = os.path.join(image_pth)
        #with open(upload_path, "wb") as file_obj:
        with open(f"{os.path.join(upload_path, files.filename)}", "wb") as file_obj:
            file_obj.write(files.file.read())

    else:
        profile_images_path = None
        profile_image_name = None
    
    user_data = {
        "email": email,
        "username": username,
        #"firebase_token": firebase_token,
        "password": password,
        "socialKind": socialKind,
        "phone_number": phone_number,
        "latitude": latitude,
        "longtitude": longtitude,
        "self_intro": self_intro,
        "profile_images_path": profile_images_path,
        "profile_image_name": profile_image_name,
    }

    # Check if the email already exists in the database
    query = db.query(models.User).filter(models.User.email == user_data["email"])

    
    if query.first() is not None:
        #raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The {user_data['email']} email is already exist!!!")
        response_content = {"user_id": None, "status": 3}
        return JSONResponse(content=response_content, status_code=409)
    #Hash the user's password
    hashed_password = await utils.hash(user_data["password"])

        


    # Create a new User instance with the provided user details
    user = models.User(
        email=user_data["email"],
        #firebase_token=user_data["firebase_token"],
        username=user_data["username"],
        password=hashed_password,
        socialKind=user_data["socialKind"],
        phone_number=user_data["phone_number"],
        latitude = user_data["latitude"],
        longtitude = user_data["longtitude"],
        self_intro = user_data["self_intro"],
        profile_images_path=user_data["profile_images_path"],
        profile_image_name=user_data["profile_image_name"],
    )
    
    # Add the user to the database
    db.add(user)
    
    # Commit the changes to the database
    db.commit()
    
    # Refresh the user object to ensure that the object in memory is up-to-date with the database
    db.refresh(user)
    
    #return user
    response_content = {"user_id": user.user_id, "status": 0}
    return JSONResponse(content=response_content, status_code=200)

@router.get("/searchById")
async def get_user_info(
        user_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(oauth2.get_current_user)
    ):
        user_info = db.query(
            models.User.username,
            models.User.latitude,
            models.User.longtitude,
            models.User.profile_images_path,
            models.User.profile_image_name
        ).filter(models.User.id == user_id).first()
                 
        if not user_info:
            return {"error": "User Info not found"}
        
        if user_info.profile_images_path is None and user_info.profile_image_name is None:

            response_data = {
            "name": user_info[0],
            "latitude": user_info[1],
            "longtitude": user_info[2]
        }
            
        else:
        
        
            #image_path = f"/home/superswing/superswing_api/profile_image/{user_info.profile_images_path}/{user_info.profile_image_name}"
            
            image_path = f"http://192.168.0.32:8010/api/avatar/{user_info.profile_images_path}/{user_info.profile_image_name}"

            with open(image_path, "rb") as file:
                file_content = base64.b64encode(file.read()).decode()

            response_data = {
                "username": user_info[0],
                "latitude": user_info[1],
                "longtitude": user_info[2],
                #"profile_image_path":user_info[3],
                "image": image_path
            }

        return response_data



@router.post('/signIn', response_model=schemas.Token, summary="Generate Token")
async def token(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Query the user by email
    user = db.query(models.User).filter(models.User.email == user_credentials.username)

    
    # Check if user exists in database
    if not user.first():
        #raise HTTPException(status_code=404, detail={"access_token": None, "token_type": None, "user_id": None})
        response_content = {"access_token": None, "token_type": None, "user_id": None, "status": 2}
        return JSONResponse(content=response_content, status_code=404)
    # Verify user's password
    verify = await utils.verify(user_credentials.password, user.first().password)

    # Raise error if verification failed
    if not verify:
        #raise HTTPException(status_code=403, detail={"access_token": None, "token_type": None, "user_id": None})
        response_content = {"access_token": None, "token_type": None, "user_id": None, "status": 1}
        return JSONResponse(content=response_content, status_code=403)
    
    # Create access token with user_id payload
    user_id = user.first().user_id
    access_token = await oauth2.create_access_token(data={"user_id": user.first().user_id})

    # Update user's last_login time in database
    user.update({"reg_dt": datetime.now()}, synchronize_session = False)
    db.commit()

    # Return access token
    #return {"access_token": access_token, "token_type": "bearer", "user_id": user_id}
    response_content = {"access_token": access_token, "token_type": "bearer", "user_id": user_id, "status": 0}
    return JSONResponse(content=response_content, status_code=200)



@router.get("/myProfile", response_model=schemas.UserReturn)
async def current_user(
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):

    user_info = db.query(
            models.User
        ).filter(
            models.User.id == current_user.user_id
        ).first()
    
    if not user_info:
        return JSONResponse(content={"detail": "User not found"}, status_code=404)
    
    image_path = f"http://192.168.0.32:8010/api/avatar/{user_info.profile_images_path}/{user_info.profile_image_name}"

    # athlete_info = db.query(
    #     models.AthleteAnalysis
    # ).join(
    #     models.AthleteVideoResult, models.AthleteVideoResult.athleteVideoResult_id == models.AthleteAnalysis.athlete_analysis_id,
    # ).filter(
    #     models.AthleteAnalysis.owner_id == current_user.user_id,
    #     models.AthleteVideoResult.athleteVideoResult_file_ext == "mp4",
    # ).order_by(
    #     models.AthleteAnalysis.analysis_reg_dt.desc()
    # ).first()

    # athlete_name = None
    # if athlete_info:
    #     athlete_name = athlete_info.athlete_name

    response_content = {
        "user_id": user_info.user_id,
        "email": user_info.email,
        "social_kind": user_info.socialKind,
        "name": user_info.username,
        "geolat": user_info.latitude,
        "geolng": user_info.longtitude,
        "self_intro": user_info.self_intro,
        "profile_image_url": image_path if user_info.profile_images_path and user_info.profile_image_name else None,
        "status": 0
    }
    return JSONResponse(content=response_content, status_code=200)
    # if athlete_info is not None:
    #     athlete_name = athlete_info[0]
    # else:
    #     athlete_name = None

    # if user_info.self_intro is None:
    #     response_content = {
    #         "user_id": user_info[0],
    #         "email": user_info[1],
    #         "social_kind": user_info[2],
    #         "name": user_info[3],
    #         "gender": user_info[4],
    #         "level": user_info[5],
    #         "self_intro": None,
    #         "profile_image_url": None,
    #         "athlete_name": athlete_name,
    #         "status": 0
    #     }
        
    # if user_info.profile_images_path is None and user_info.profile_image_name is None:
    #     response_content = {
    #         "user_id": user_info[0],
    #         "email": user_info[1],
    #         "social_kind": user_info[2],
    #         "name": user_info[3],
    #         "gender": user_info[4],
    #         "level": user_info[5],
    #         "profile_image_url": None,
    #         "athlete_name": athlete_name,
    #         "status": 0
    #     }
    # else:
    #     image_path = f"http://192.168.0.32:8010/api/avatar/{user_info.profile_images_path}/{user_info.profile_image_name}"
    #     response_content = {
    #         "user_id": user_info[0],
    #         "email": user_info[1],
    #         "social_kind": user_info[2],
    #         "name": user_info[3],
    #         "gender": user_info[4],
    #         "level": user_info[5],
    #         "profile_image_url": image_path,
    #         "athlete_name": athlete_name,
    #         "status": 0
    #     }

    

@router.post("/nickname")#, response_model = schemas.NicknameExist)
async def check_nickname(
    name: str,
    db: Session = Depends(database.get_db)):
    
    query = db.query(models.User).filter(models.User.name == name)
    if query.first() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The {name} name is already exist!!!")
    else:
        #return{"message": f"The {name} name is available."}
        return True
    
