from fastapi import status, HTTPException, Depends, APIRouter, Query
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas, crud
from ..database import get_db
from typing import List
import typing as t
from fastapi.responses import JSONResponse
import base64
from ..config import settings
from geopy.distance import geodesic
import time

router = APIRouter()

# Rate limiter configuration
RATE_LIMIT = 10  # Number of allowed requests
TIME_WINDOW = 60  # Time window in seconds

# In-memory store for rate limiting (use Redis or similar for production)
request_times = {}

def rate_limiter(USER_ID: int):
    current_time = time.time()

    # Initialize user's request times if not present
    if USER_ID not in request_times:
        request_times[USER_ID] = []

    # Filter out requests outside the time window
    request_times[USER_ID] = [timestamp for timestamp in request_times[USER_ID] if current_time - timestamp < TIME_WINDOW]

    # Check if the number of requests is within the limit
    if len(request_times[USER_ID]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests, please try again later.")

    # Add the current request timestamp
    request_times[USER_ID].append(current_time)

@router.get("/myNodes", response_model=t.List[schemas.NodesReturn])
async def get_only_my_nodes_endpoint(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    rate_limiter(current_user.USER_MNG_ID)
    nodes = await crud.get_only_my_nodes(db, user_id=current_user.USER_MNG_ID)
    return nodes

@router.get("/userNodes", response_model=t.List[schemas.NodesReturn])
async def get_only_user_nodes_endpoint(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
):
    rate_limiter(current_user.USER_MNG_ID)
    nodes = await crud.get_only_user_nodes(db, user_id=current_user.USER_MNG_ID)
    return nodes

@router.get("/searchNodesTitle", response_model=List[schemas.NodesReturn])
async def search_nodes_by_title(
    title: str,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
):
    rate_limiter(current_user.USER_MNG_ID)
    nodes = await crud.search_nodes_by_title(db, user_id=current_user.USER_MNG_ID, title=title)
    return nodes

@router.get("/{id}", response_model=schemas.NodeReturn, status_code=status.HTTP_201_CREATED)
async def get_node_by_id_endpoint(
    id: str,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
):
    rate_limiter(current_user.USER_MNG_ID)
    node = await crud.get_node_by_id(db, id)
    if not node:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Node not found"})
    
    # Construct the URL using node_json_path and node_json_name
    #json_url = f"http://192.168.0.130:8010/api/json/{node.node_json_path}/{node.node_json_name}"
    json_url = f"{settings.nodes_folder}/{node.NODE_JSON_PATH}/{node.NODE_JSON_NAME}"

    with open(json_url, "rb") as file:
        json_file = base64.b64encode(file.read()).decode()

    # Convert node to dictionary and add the json_url
    node_dict = node.__dict__
    node_dict['json_file'] = json_file

    # Remove the sqlalchemy internal attributes
    node_dict.pop('_sa_instance_state', None)

    return node_dict

@router.put("/{id}", response_model=schemas.UpdatedNode, status_code=status.HTTP_201_CREATED)
async def update_node_endpoint(
    id: str, 
    node: schemas.NodeUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.require_user)
    ):
    rate_limiter(current_user.USER_MNG_ID)
    updated_node = await crud.node_update(db, id, current_user.USER_MNG_ID, node)
    return updated_node

@router.post("/", response_model=List[schemas.SearchNode], status_code=status.HTTP_200_OK)
async def search_nodes_on_map(
    request: schemas.NodeSearchRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.require_user)
):
    rate_limiter(current_user.USER_MNG_ID)
    latitude = request.LATITUDE
    longitude = request.LONGITUDE
    nodes_with_distance = await crud.get_nodes_on_map(db, latitude, longitude)
    search_nodes = [
        schemas.SearchNode(
            NODE_ID=node['node'].NODE_ID,
            USER_MNG_ID=node['node'].USER_MNG_ID,
            ASSET_ID=node['node'].ASSET_ID,
            NODE_TITLE=node['node'].NODE_TITLE,
            NODE_DESCRIPTION=node['node'].NODE_DESCRIPTION,
            LATITUDE=node['node'].LATITUDE,
            LONGITUDE=node['node'].LONGITUDE,
            DISTANCE=node['distance']
        )
        for node in nodes_with_distance
    ]
    return search_nodes