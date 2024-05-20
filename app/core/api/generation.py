from fastapi import status, Depends, APIRouter
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
from ..config import settings
from uuid import uuid4
#from pyrebase4 import pyrebase


timestr = time.strftime("%Y%m%d-%H%M%S")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR,"uploads")

# Create a router instance
router = APIRouter()



@router.post("/Object", status_code=status.HTTP_201_CREATED)
async def generate_object(
    object_title: str,
    object_description: str,
    object_type: str,
    fileUpload_file_count: int,
    fileUpload_conversion_type: str,
    fileUpload_status: str,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user),
):
    try:
        user_id = current_user.user_id

        fileUpload_uuid = uuid.uuid4().hex
        
        current_date = str(datetime.now().strftime("%Y-%m-%d"))

        fileUpload_folder_path = os.path.join(settings.files_folder, current_date, fileUpload_uuid)
        os.makedirs(fileUpload_folder_path, exist_ok=True)
      
        fileUpload_records = []

        for file in files:
            fileUpload_filename = os.path.basename(file.filename)

            pth = fileUpload_folder_path.replace("\\","/")
            sub_pth = pth.split("/")
            final_pth = f'{sub_pth[len(sub_pth)-2]}/{sub_pth[len(sub_pth)-1]}'
            fileUpload_path = os.path.join(final_pth)
            
            with open(f"{os.path.join(fileUpload_folder_path, file.filename)}", "wb") as file_obj:
                file_obj.write(file.file.read())

        fileUpload = {
                "fileUpload_uuid": fileUpload_uuid,
                "fileUpload_path": fileUpload_path,
                "fileUpload_filename": fileUpload_filename,
                "fileUpload_file_count": fileUpload_file_count,
                "fileUpload_conversion_type": fileUpload_conversion_type,
                "fileUpload_status": fileUpload_status,
                "owner_id": user_id
            }

        
        new_fileUpload= models.FileUpload(**fileUpload)
        fileUpload_records.append(new_fileUpload)

        # Add all file upload records to the database
        db.add_all(fileUpload_records)
        db.commit()

        # Retrieve the fileUpload_id of the first record (assuming it's a single file upload)
        fileUpload_id = fileUpload_records[0].fileUpload_id

        
        object = {
                "id": fileUpload_id,
                "user_id": user_id,
                "object_title": object_title,
                "object_description": object_description,
                "object_type": object_type,
                "status": fileUpload_status,
                "object_uuid": fileUpload_uuid,
        }
        
        new_object = models.Object(**object)
        db.add(new_object)
        db.commit()

        # Enqueue the asset details for further processing
        enqueue_fileUploads(fileUpload_records, settings.queue_folder, current_date, object_title, object_type)

        return fileUpload_records[0].fileUpload_id
    except Exception as e:
        db.rollback()
        
        raise


def enqueue_fileUploads(fileUpload_records: List[models.FileUpload], QUEUE_FOLDER: str, current_date, object_title: str, object_type: str,):
    try:
        # Create a list to store file paths for all files
        file_paths = []

        # Save asset details as JSON files in the queue folder
        os.makedirs(QUEUE_FOLDER, exist_ok=True)
        for fileUpload in fileUpload_records:
            pth = fileUpload.fileUpload_path.replace("\\", "/")
            sub_pth = pth.split("/")
            final_pth = f'{sub_pth[len(sub_pth) - 2]}/{sub_pth[len(sub_pth) - 1]}'
            file_paths.append(final_pth)

            # Send data to Firebase
            #send_to_firebase(fileUpload, final_pth, current_date, )

        # Create a dictionary with the combined data
        combined_data = {
            "asset_id": fileUpload.fileUpload_id,
            "assetTitle": object_title,
            "fileType": object_type,
            "fileCount": fileUpload.fileUpload_file_count,
            "filePath": final_pth,
            "conversion_type": fileUpload.fileUpload_conversion_type,
            "status": fileUpload.fileUpload_status,
            "uuid": fileUpload.fileUpload_uuid,
            "owner_id": fileUpload.owner_id
           }

        # Create a single JSON file for all file upload data
        combined_json_path = os.path.join(QUEUE_FOLDER, f"{fileUpload.fileUpload_uuid}.json")
        with open(combined_json_path, "w") as combined_json_file:
            json.dump(combined_data, combined_json_file)
    except Exception as e:
        # Handle the exception (e.g., log the error)
        raise


# config = {
#     "apiKey": "AIzaSyBdfWKKmCF0pUU9xYALVKmMjeMr3hTDOz0",
#     "authDomain": "mobile-app-3d.firebaseapp.com",
#     "databaseURL": "https://mobile-app-3d-default-rtdb.asia-southeast1.firebasedatabase.app",
#     "projectId": "mobile-app-3d",
#     "storageBucket": "mobile-app-3d.appspot.com",
#     "messagingSenderId": "565457998500",
#     "appId": "1:565457998500:web:6519bcca1c26254be90c31",
#     "measurementId": "G-QYLF45D2Z7"
# }

# # Initialize Pyrebase with your config
# firebase = pyrebase.initialize_app(config)

# # Get a reference to the database
# db = firebase.database()
# def send_to_firebase(fileUpload, final_pth, current_date, object_title):

#     try:
#         db = firebase.database()

#         data_to_push = {
            
#             "asset_id": fileUpload.fileUpload_id,
#             "asset_title": object_title,
#             "file_path": final_pth,
#             "status": 0,
#             "update_dt": current_date
#         }
        
#         db.child("assets").child(f"{fileUpload.fileUpload_owner_id}").child(f"{fileUpload.fileUpload_id}").set(data=data_to_push)
        
#     except Exception as e:
#         # Handle the exception (e.g., log the error)
#         raise