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


timestr = time.strftime("%Y%m%d-%H%M%S")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR,"uploads")

# Create a router instance
router = APIRouter()

OBJECTS_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/objects"
NODES_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/nodes"
QUEUE_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/queue"
RESULT_FOLDER = "C:/Users/USER/Desktop/anchorWorld_auth/video_results"



# Asset creation route
@router.post("/Object", status_code=status.HTTP_201_CREATED)
async def upload_object(
    title: str,
    description: str,
    object_type: str,
    status: str,
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user),
    ):
    try:
        
       
        user_id = current_user.user_id  # Create a new asset in the database
        
        object_uuid = uuid.uuid4().hex # Generate a UUID for the asset
        
        current_date = str(datetime.now().strftime("%Y-%m-%d")) # Generate the current date as string

        object_file_name = os.path.basename(file.filename)

        object_folder_path = os.path.join(OBJECTS_FOLDER, current_date, object_uuid) # Create a folder to save the files
        os.makedirs(object_folder_path, exist_ok=True)

        object_records = []  # Save uploaded files to the folder
        
        pth = object_folder_path.replace("\\", "/")
        sub_pth = pth.split("/")
        final_pth = f'{sub_pth[len(sub_pth)-2]}/{sub_pth[len(sub_pth)-1]}'
        object_file_path = os.path.join(final_pth)

        #fileUpload_file_size = os.path.getsize(os.path.join(fileUpload_folder_path, file.filename))

        _, file_ext = os.path.splitext(file.filename)

        with open(f"{os.path.join(object_folder_path, file.filename)}", "wb") as file_obj:
            file_obj.write(file.file.read())

        object = {
            "object_title": title, 
            "object_description": description,
            "object_type": object_type,
            "status": status, 
            "object_file_path": object_file_path,
            "object_uuid": object_uuid,
            "object_file_name": object_file_name,
            "file_ext": file_ext, 
            "user_id": user_id
        }

        
        new_object= models.Object(**object)
        object_records.append(new_object)

        # Add all file upload records to the database
        db.add_all(object_records)
        db.commit()
        
        return object_records[0].id
    except Exception as e:
        db.rollback()
        # Handle the exception (e.g., log the error)
        raise

@router.post("/Anchor", status_code=status.HTTP_201_CREATED)
async def upload_anchor(
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    try:
        user_id = current_user.user_id

        node_json_uuid = uuid.uuid4().hex
        current_date = str(datetime.now().strftime("%Y-%m-%d"))

        node_json_name = os.path.basename(file.filename)

        node_file_path = os.path.join(NODES_FOLDER, current_date, node_json_uuid)
        os.makedirs(node_file_path, exist_ok=True)

        # Modify node_json_path to desired format
        node_json_path = f"{current_date}/{node_json_uuid}"

        with open(os.path.join(node_file_path, node_json_name), "wb") as file_obj:
            file_content = await file.read()
            file_obj.write(file_content)

        json_data = json.loads(file_content.decode('utf-8'))

        # Extracting information from JSON data
        node_name = json_data["data"]["name"]
        anchor_data = json_data["data"]["childNodes"][0]
        title = anchor_data.get("name", str(uuid4()))  # Generate UUID if anchor name is empty
        latitude = anchor_data["position"]["geopoint"]["latitude"]
        longitude = anchor_data["position"]["geopoint"]["longitude"]
        status_value = json_data["data"]["status"]
        hashtags = json_data["data"]["hashtags"]
        object_id = json_data["data"]["uri"]

        # Check if anchor already exists, if not, insert into Anchor table
        existing_anchor = db.query(models.Anchor).filter(models.Anchor.anchor_title == title).first()
        if not existing_anchor:
            new_anchor = models.Anchor(
                anchor_title=title,
                latitude=latitude,
                longitude=longitude,
                status=status_value
            )
            db.add(new_anchor)
            db.commit()
            db.refresh(new_anchor)

        # Creating node record
        node = {
            "node_title": node_name,
            "node_description": json_data["data"]["onTapText"],
            "latitude": latitude,
            "longitude": longitude,
            "object_id": object_id,
            "status": status_value,
            "user_id": user_id,
            "node_json_path": node_json_path,
            "node_json_name": node_json_name
        }
        new_node = models.Node(**node)
        db.add(new_node)
        db.commit()

        return new_node.id
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))