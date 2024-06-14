from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
from ..database import get_db
from fastapi import File, UploadFile
import json 
import os
import time
import uuid
from .. import models, oauth2
from datetime import datetime
from uuid import uuid4
from ..config import settings
import time
import logging

timestr = time.strftime("%Y%m%d-%H%M%S")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR,"uploads")

# Create a router instance
router = APIRouter()




# Asset creation route
@router.post("/Object", status_code=status.HTTP_201_CREATED)
async def upload_object(
    ASSET_TITLE: str,
    DESCRIPTION: str,
    ASSET_TYPE: str,
    PUBLIC_YN: str,
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.require_user),
    ):
    try:
        USER_MNG_ID = current_user.USER_MNG_ID
        file_uuid = uuid.uuid4().hex
        ASSET_ID = uuid.uuid4().hex
        current_date = str(datetime.now().strftime("%Y-%m-%d"))
        orgn_file_nm = os.path.basename(file.filename)
        object_folder_path = os.path.join(settings.objects_folder, current_date, file_uuid)
        os.makedirs(object_folder_path, exist_ok=True)

        assetStore_records = []
        fileMaster_records = []
        fileModel_records = []

        pth = object_folder_path.replace("\\", "/")
        sub_pth = pth.split("/")
        final_pth = f'{sub_pth[len(sub_pth)-2]}/{sub_pth[len(sub_pth)-1]}'
        asset_file_path = os.path.join(final_pth)

        _, FILE_EXT = os.path.splitext(file.filename)

        # Read the file content
        file_content = await file.read()
        FILE_SIZE = len(file_content)

        with open(f"{os.path.join(object_folder_path, file.filename)}", "wb") as file_obj:
            file_obj.write(file_content)  # Use the already read file content

        fileMaster = {
            "USER_MNG_ID": USER_MNG_ID,
            "FILE_UUID": file_uuid,
            "UPLOAD_STATUS_CD": "03",
            "UPLOAD_FILE_COUNT": 1,
            "UPLOAD_FILE_PATH": asset_file_path,
            "NERF_STATUS_CD": "03",
            "NERF_FILE_PATH": asset_file_path,
            "CNVRT_CPTN_DT": current_date,
            "REG_USER_ID": current_user.USER_ID,
            "MOD_USER_ID": current_user.USER_ID,
        }

        new_fileMaster = models.FileMaster(**fileMaster)
        fileMaster_records.append(new_fileMaster)
        db.add_all(fileMaster_records)

        assetStore = {
            "ASSET_ID": ASSET_ID,
            "ASSET_TITLE": ASSET_TITLE,
            "USER_MNG_ID": USER_MNG_ID,
            "CTGRY_CD": "CT_CRNV",
            "CPRT_CD": "CPRT0003",
            "CVTT_CD": "CVTT0005",
            "ASPR_CD": "ASPR0001",
            "DESCRIPTION": DESCRIPTION,
            "PUBLIC_YN": PUBLIC_YN,
            "ASSET_TYPE": ASSET_TYPE,
            "PICK_YN": "N",
            "READ_CNT": 0,
            "LIKE_CNT": 0,
            "FILE_UUID": file_uuid,
            "THUM_MODEL_ID": None,
            "COMMENT_YN": "Y",
            "TEXTURE_YN": "N",
            "TASK_TYPE": "ANCHOR",
            "REG_USER_ID": current_user.USER_ID,
            "MOD_USER_ID": current_user.USER_ID,
            "ASSET_TYPE": ASSET_TYPE,
        }

        new_assetStore = models.AssetStore(**assetStore)
        assetStore_records.append(new_assetStore)
        db.add_all(assetStore_records)

        fileModel = {
            "FILE_UUID": file_uuid,
            "ORGN_FILE_NM": orgn_file_nm,
            "CHNG_FILE_NM": orgn_file_nm,
            "FILE_SEQ": 0,
            "FILE_EXT": FILE_EXT,
            "FILE_SIZE": FILE_SIZE,
            "FILE_UPLOAD_YN": "Y",
            "CTGRY_CD": "CT_CRNV",
            "REG_USER_ID": current_user.USER_ID,
            "MOD_USER_ID": current_user.USER_ID,
        }

        new_fileModel = models.FileModel(**fileModel)
        fileModel_records.append(new_fileModel)
        db.add_all(fileModel_records)

        db.commit()

        return assetStore_records[0].FILE_UUID

    except Exception as e:
        db.rollback()
        logging.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/Anchor", status_code=status.HTTP_201_CREATED)
async def upload_anchor(
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.require_user)
):
    try:
        USER_MNG_ID = current_user.USER_MNG_ID
        ANCHOR_ID = uuid.uuid4().hex
        NODE_ID = uuid.uuid4().hex

        node_json_uuid = uuid.uuid4().hex
        current_date = str(datetime.now().strftime("%Y-%m-%d"))

        NODE_JSON_NAME = os.path.basename(file.filename)

        node_file_path = os.path.join(settings.nodes_folder, current_date, node_json_uuid)
        os.makedirs(node_file_path, exist_ok=True)

        # Modify node_json_path to desired format
        NODE_JSON_PATH = f"{current_date}/{node_json_uuid}"

        with open(os.path.join(node_file_path, NODE_JSON_NAME), "wb") as file_obj:
            file_content = await file.read()
            file_obj.write(file_content)

        json_data = json.loads(file_content.decode('utf-8'))

        # Extracting information from JSON data
        node_name = json_data["data"]["node_title"]
        title = json_data["data"]["anchor_title"]
        latitude = json_data["data"]["lat"]
        longitude = json_data["data"]["long"]
        status_value = json_data["data"]["status"]
        hashtags = json_data["data"]["hashtags"]
        object_id = json_data["data"]["object_id"]
        node_description = json_data["data"]["description"]
        anchor_uuid = json_data["data"]["uuid"]

        # Check if anchor already exists, if not, insert into Anchor table
        existing_anchorStore = db.query(models.AnchorStore).filter(models.AnchorStore.ANCHOR_TITLE == title).first()
        if not existing_anchorStore:
            new_anchorStore = models.AnchorStore(
                ANCHOR_ID=ANCHOR_ID,
                ANCHOR_TITLE=title,
                USER_MNG_ID=USER_MNG_ID,
                LATITUDE=latitude,
                LONGITUDE=longitude,
                PUBLIC_YN=status_value,
                REG_USER_ID=current_user.USER_ID,
                MOD_USER_ID=current_user.USER_ID,
                ANCHOR_UUID=anchor_uuid,
            )
            db.add(new_anchorStore)
            db.commit()
            db.refresh(new_anchorStore)

        # Creating node record
        nodeStore = {
            "NODE_ID": NODE_ID,
            "NODE_TITLE": node_name,
            "NODE_DESCRIPTION": node_description,
            "LATITUDE": latitude,
            "LONGITUDE": longitude,
            "ASSET_ID": object_id,
            "PUBLIC_YN": status_value,
            "USER_MNG_ID": USER_MNG_ID,
            "NODE_JSON_PATH": NODE_JSON_PATH,
            "NODE_JSON_NAME": NODE_JSON_NAME,
            "REG_USER_ID": current_user.USER_ID,
            "MOD_USER_ID": current_user.USER_ID,
            "ANCHOR_UUID": anchor_uuid,
        }
        new_nodeStore = models.NodeStore(**nodeStore)
        db.add(new_nodeStore)
        db.commit()

        return new_nodeStore.ANCHOR_UUID
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@router.post("/Video", status_code=status.HTTP_201_CREATED)
async def upload_video(
    VIDEO_TITLE: str,
    VIDEO_DESCRIPTION: str,
    NODE_ID: str,
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.require_user),
    ):
    try:
        USER_MNG_ID = current_user.USER_MNG_ID  # Create a new asset in the database
        
        
        video_uuid = uuid.uuid4().hex # Generate a UUID for the asset
        VIDEO_ID = uuid.uuid4().hex

        current_date = str(datetime.now().strftime("%Y-%m-%d")) # Generate the current date as string

        VIDEO_FILE_NAME = os.path.basename(file.filename)

        video_folder_path = os.path.join(settings.video_folder, current_date, video_uuid) # Create a folder to save the files
        os.makedirs(video_folder_path, exist_ok=True)

        videoStore_records = []  # Save uploaded files to the folder
        
        pth = video_folder_path.replace("\\", "/")
        sub_pth = pth.split("/")
        final_pth = f'{sub_pth[len(sub_pth)-2]}/{sub_pth[len(sub_pth)-1]}'
        VIDEO_FILE_PATH = os.path.join(final_pth)

        _, file_ext = os.path.splitext(file.filename)

        with open(f"{os.path.join(video_folder_path, file.filename)}", "wb") as file_obj:
            file_obj.write(file.file.read())

        ASSET_ID_query = db.query(
            models.NodeStore.ASSET_ID,
            models.NodeStore.PUBLIC_YN
            ).filter(
                models.NodeStore.NODE_ID == NODE_ID
            ).first()

        videoStore = {
            "VIDEO_ID": VIDEO_ID,
            "ASSET_ID": ASSET_ID_query[0],
            "VIDEO_TITLE": VIDEO_TITLE, 
            "USER_MNG_ID": USER_MNG_ID,
            "VIDEO_DESCRIPTION": VIDEO_DESCRIPTION,            
            "NODE_ID": NODE_ID,
            "REG_USER_ID": current_user.USER_ID,
            "MOD_USER_ID": current_user.USER_ID,
            "VIDEO_FILE_PATH": VIDEO_FILE_PATH,
            "VIDEO_FILE_NAME": VIDEO_FILE_NAME,
            "PUBLIC_YN": ASSET_ID_query[1],
        }

        
        new_videoStore= models.VideoStore(**videoStore)
        videoStore_records.append(new_videoStore)

        # Add all file upload records to the database
        db.add_all(videoStore_records)
        db.commit()
        
        return videoStore_records[0].VIDEO_ID
    except Exception as e:
        db.rollback()
        # Handle the exception (e.g., log the error)
        raise