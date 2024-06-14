from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas, crud
from ..database import get_db
from typing import List
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


@router.get("/anchorList", response_model=List[schemas.AnchorList], status_code=status.HTTP_200_OK)
async def get_anchor_list(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.require_user)
):
    anchor_list = db.query(
        models.AnchorStore
        ).filter(
        models.AnchorStore.PUBLIC_YN == "Y"
        ).all()
    return anchor_list


@router.post("/", response_model=List[schemas.SearchAnchor], status_code=status.HTTP_200_OK)
async def search_anchors_on_map(
    request: schemas.NodeSearchRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.require_user)
):
    rate_limiter(current_user.USER_MNG_ID)
    latitude = request.LATITUDE
    longitude = request.LONGITUDE
    anchors_with_distance = await crud.get_anchors_on_map(db, latitude, longitude)
    search_anchors = [
        schemas.SearchAnchor(
            ANCHOR_ID=anchor['anchor'].ANCHOR_ID,
            USER_MNG_ID=anchor['anchor'].USER_MNG_ID,
            ANCHOR_TITLE=anchor['anchor'].ANCHOR_TITLE,
            LATITUDE=anchor['anchor'].LATITUDE,
            LONGITUDE=anchor['anchor'].LONGITUDE,
            DISTANCE=anchor['distance']
        )
        for anchor in anchors_with_distance
    ]
    return search_anchors