from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas
from ..database import get_db
from typing import List

router = APIRouter()


@router.get("/anchorList", response_model=List[schemas.AnchorList])
async def get_anchor_list(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    anchor_list = db.query(
        models.Anchor
        ).filter(
        models.Anchor.status == "public"
        ).all()
    return anchor_list


@router.get("/anchorsNearByMe", response_model=List[schemas.AnchorNearByMe])
async def get_anchors_near_by_me(
    latitude: str,
    longitude: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    anchors = db.query(
        models.Anchor
        ).filter(
            models.Anchor.status =="public",
            models.Anchor.latitude == latitude,
            models.Anchor.longitude == longitude
        ).all()
    return anchors