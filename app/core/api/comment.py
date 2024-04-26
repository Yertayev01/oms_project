from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas, crud
from ..database import get_db
from typing import List

router = APIRouter()



@router.get("/getObjects", response_model=List[schemas.ObjectCommentReturn])
async def get_all_object_comments(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    comments = await crud.get_object_comments(db)
    return comments

@router.get("/getNodes", response_model=List[schemas.NodeCommentReturn])
async def get_all_Node_comments(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    comments = await crud.get_node_comments(db)
    return comments


@router.post("/postObjectComment", status_code=status.HTTP_201_CREATED)
async def comment_object(
    comment: schemas.ObjectCommentCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    created_comment = await crud.post_object_comment(db, comment, current_user.user_id)
    return created_comment


@router.post("/postNodeComment", status_code=status.HTTP_201_CREATED)
async def comment_node(
    comment: schemas.ObjectCommentCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    created_comment = await crud.post_node_comment(db, comment, current_user.user_id)
    return created_comment


@router.get("/object/{comment_id}", response_model=schemas.ObjectCommentReturn)
async def get_object_comment_by_id(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    comment = await crud.get_object_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment

@router.get("/node/{comment_id}", response_model=schemas.NodeCommentReturn)
async def get_node_comment_by_id(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    comment = await crud.get_node_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.put("/objectUpdate/{comment_id}", response_model=schemas.ObjectCommentReturn)
async def object_update_comment(
    comment_id: int,
    comment: schemas.ObjectCommentUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    updated_comment = await crud.object_comment_update(db, comment_id, current_user.user_id, comment)
    return updated_comment


@router.put("/nodeUpdate/{comment_id}", response_model=schemas.NodeCommentReturn)
async def node_update_comment(
    comment_id: int,
    comment: schemas.NodeCommentUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    updated_comment = await crud.node_comment_update(db, comment_id, current_user.user_id, comment)
    return updated_comment


@router.delete("/objectDelete/{comment_id}", response_model=schemas.ObjectCommentReturn, status_code=status.HTTP_202_ACCEPTED)
async def object_delete_comment(
    id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    deleted_comment = await crud.object_comment_delete(db, id)
    return deleted_comment


@router.delete("/nodeDelete/{comment_id}", response_model=schemas.NodeCommentReturn, status_code=status.HTTP_202_ACCEPTED)
async def node_delete_comment(
    id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.require_user)
):
    deleted_comment = await crud.node_comment_delete(db, id)
    return deleted_comment