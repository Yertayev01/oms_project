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

@router.get("/", response_model=t.List[schemas.NodesReturn])
async def get_all_nodes_endpoint(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    nodes = await crud.get_nodes(db)

    return nodes

@router.get("/myNodes", response_model=t.List[schemas.NodesReturn])
async def get_only_my_nodes_endpoint(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    nodes = await crud.get_only_my_nodes(db, user_id=current_user.user_id)
    return nodes

@router.get("/userNodes", response_model=t.List[schemas.NodesReturn])
async def get_only_user_nodes_endpoint(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    nodes = await crud.get_only_user_nodes(db)
    return nodes

@router.get("/{id}", response_model=schemas.NodeReturn, status_code=status.HTTP_201_CREATED)
async def get_node_by_id_endpoint(
    id: int,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
):
    node = await crud.get_node_by_id(db, id)
    if not node:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Node not found"})
    
    # Construct the URL using node_json_path and node_json_name
    #json_url = f"http://192.168.0.130:8010/api/json/{node.node_json_path}/{node.node_json_name}"
    json_url = f"C:/Users/USER/Desktop/anchorWorld_auth/nodes/{node.node_json_path}/{node.node_json_name}"

    with open(json_url, "rb") as file:
        json_file = base64.b64encode(file.read()).decode()

    # Convert node to dictionary and add the json_url
    node_dict = node.__dict__
    node_dict['json_file'] = json_file

    # Remove the sqlalchemy internal attributes
    node_dict.pop('_sa_instance_state', None)

    return node_dict

@router.put("/{id}", response_model=schemas.NodeReturn, status_code=status.HTTP_201_CREATED)
async def update_node_endpoint(
    id: int, 
    node: schemas.NodeUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    node = await crud.node_update(db, id, current_user.user_id, node)
    return node