from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core import models, schemas, utils
from sqlalchemy import func
import math
from sqlalchemy import and_
import re
#from app.core.utils import hash_password

#user
async def get_user_by_id(db: Session, user_id: str) -> models.User:
    return db.query(models.User).filter(models.User.USER_ID == user_id).first()

async def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.USER_NM == username).first()

async def get_users(db: Session) -> List[models.User]:
    return db.query(models.User).all()

async def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.USER_NM == username).first()

async def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.EMAIL == email).first()

async def user_create(db: Session, user: schemas.UserCreate) -> models.User:
    # Check if email exists
    existing_email = await get_user_by_email(db, user.EMAIL)
    if existing_email:
        raise HTTPException(detail=f"Email {user.EMAIL} is already registered", status_code=status.HTTP_409_CONFLICT)

    # Check if username exists
    existing_username = await get_user_by_username(db, user.USER_NM)
    if existing_username:
        raise HTTPException(detail=f"Username {user.USER_NM} is already taken", status_code=status.HTTP_409_CONFLICT)
    
    user.PSSWRD = await utils.hash_password(user.PSSWRD)
    db_user = models.User(
        **user.dict(),
    )

    user.REG_USER_ID = user.USER_ID
    user.MOD_USER_ID = user.USER_ID

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def user_update(db: Session, user_id: int, user: schemas.UserUpdate) -> models.User:
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = await utils.hash_password(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def user_delete(db: Session, user_id: int) -> models.User:
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

#photo
async def photo_create(db: Session, photo: schemas.PhotoCreate):
    photo = models.Photo(
        **photo.dict()
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

#asset
async def get_asset_by_id(db: Session, id: str):
    return db.query(
        models.FileMaster.NERF_FILE_PATH,
        models.FileModel.CHNG_FILE_NM,
    ).join(
        models.FileModel, models.FileModel.FILE_UUID == models.FileMaster.FILE_UUID,
    ).filter(
        models.FileMaster.FILE_UUID == id
    ).first()

async def get_objects(db: Session) -> List[models.AssetStore]:
    #return db.query(models.AssetStore).filter(models.AssetStore.conversion_status == '2').all()
    return db.query(models.AssetStore).all()

async def get_only_my_objects(db: Session, user_id: str, asset_type: str) -> List[models.AssetStore]:
    return db.query(models.AssetStore).filter(
        models.AssetStore.USER_MNG_ID == user_id,
        models.AssetStore.ASSET_TYPE == asset_type,
        #models.AssetStore.conversion_status == '2'
    ).all()

async def get_only_user_objects(db: Session, user_id: int, asset_type: str) -> List[models.AssetStore]:
    return db.query(models.AssetStore).filter(
        models.AssetStore.ASSET_TYPE == asset_type,
        #models.AssetStore.conversion_status == '2',
        models.AssetStore.USER_MNG_ID != user_id
    ).all()

async def object_update(db: Session, id: str, user_id: int, object: schemas.AssetUpdate) -> schemas.AssetReturn:
    db_asset = await get_asset_by_id(db, id)
    if not db_asset:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if db_asset.USER_MNG_ID != user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You are not post owner")
    
    update_data = object.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asset, key, value)

    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

#node
async def get_node_by_id(db: Session, id: str):
    return db.query(models.NodeStore).filter(models.NodeStore.NODE_ID == id).first()

async def get_nodes(db: Session) -> List[models.NodeStore]:
    return db.query(models.NodeStore).all()

async def get_only_my_nodes(db: Session, user_id: str) -> List[models.NodeStore]:
    return db.query(models.NodeStore).filter(models.NodeStore.USER_MNG_ID == user_id).all()

async def search_nodes_by_title(db: Session, user_id: str, title: str) -> List[models.NodeStore]:
    return  db.query(models.NodeStore).filter(
        and_(
            models.NodeStore.NODE_TITLE.ilike(f'%{title}%')
        )
    ).all()

async def get_only_user_nodes(db: Session, user_id: str) -> List[models.NodeStore]:
    return db.query(models.NodeStore).filter(models.NodeStore.USER_MNG_ID != user_id).all()

async def node_update(db: Session, id: int, user_id: str, node: schemas.NodeUpdate) -> schemas.UpdatedNode:
    db_node = await get_node_by_id(db, id)
    if not db_node:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Node not found")
    
    if db_node.USER_MNG_ID != user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You are not the node owner")
    
    update_data = node.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_node, key, value)

    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node


async def get_nodes_on_map(db: Session, latitude: float, longitude: float) -> List[dict]:
    
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371000  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    
    nodes = db.query(models.NodeStore).all()
    nodes_with_distance = [
        (node, calculate_distance(latitude, longitude, node.LATITUDE, node.LONGITUDE))
        for node in nodes
    ]
    nodes_with_distance.sort(key=lambda x: x[1])
    return [{'node': node, 'distance': distance} for node, distance in nodes_with_distance]


#anchor
async def get_anchors_on_map(db: Session, latitude: float, longitude: float) -> List[dict]:
    
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371000  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    
    anchors = db.query(models.AnchorStore).all()
    anchors_with_distance = [
        (anchor, calculate_distance(latitude, longitude, anchor.LATITUDE, anchor.LONGITUDE))
        for anchor in anchors
    ]
    anchors_with_distance.sort(key=lambda x: x[1])
    return [{'anchor': anchor, 'distance': distance} for anchor, distance in anchors_with_distance]

#video

async def get_video_by_id(db: Session, id: str):
    return db.query(
            models.VideoStore.VIDEO_FILE_PATH,
            models.VideoStore.VIDEO_FILE_NAME,
        ).filter(
            models.VideoStore.VIDEO_ID == id).first()

async def get_videos(db: Session) -> List[models.VideoStore]:
    return db.query(models.VideoStore).all()

async def get_only_my_videos(db: Session, user_id) -> List[models.VideoStore]:
    return db.query(models.VideoStore).join(models.NodeStore, models.NodeStore.NODE_ID == models.VideoStore.NODE_ID).filter(models.NodeStore.USER_MNG_ID == user_id).all()

async def get_only_user_videos(db: Session, user_id) -> List[models.VideoStore]:
    return db.query(models.VideoStore).join(models.NodeStore, models.NodeStore.NODE_ID == models.VideoStore.NODE_ID).filter(models.NodeStore.USER_MNG_ID != user_id).all()


async def update_video_by_id(db: Session, id: str):
    return db.query(
            models.VideoStore
        ).filter(
            models.VideoStore.VIDEO_ID == id).first()

async def video_update(db: Session, id: int, user_id: int, video: schemas.VideoUpdate) -> schemas.VideoReturn:
    db_video = await update_video_by_id(db, id)
    if not db_video:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if db_video.USER_MNG_ID != user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You are not post owner")
    
    update_data = video.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_video, key, value)

    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

# post comment
async def post_object_comment(db: Session, comment: schemas.ObjectCommentCreate, user_id):
    comment = models.AssetComments(
            **comment.dict(), user_id = user_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def post_node_comment(db: Session, comment: schemas.NodeCommentCreate, user_id):
    comment = models.NodeComments(
            **comment.dict(), user_id = user_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

#post like
async def post_object_like(db: Session, like: schemas.ObjectLikeCreate, user_id):
    like = models.AssetLikes(
            **like.dict(), user_id = user_id
    )
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

async def post_node_like(db: Session, like: schemas.NodeLikeCreate, user_id):
    like = models.NodeLikes(
            **like.dict(), user_id = user_id
    )
    db.add(like)
    db.commit()
    db.refresh(like)
    return like


#post save
async def post_object_save(db: Session, save: schemas.ObjectSaveCreate, user_id):
    save = models.AssetSaves(
            **save.dict(), user_id = user_id
    )
    db.add(save)
    db.commit()
    db.refresh(save)
    return save

async def post_node_save(db: Session, save: schemas.NodeSaveCreate, user_id):
    save = models.NodeSaves(
            **save.dict(), user_id = user_id
    )
    db.add(save)
    db.commit()
    db.refresh(save)
    return save


#get comment all
async def get_object_comments(db: Session) -> List[models.AssetComments]:
    return db.query(models.AssetComments).all()

async def get_node_comments(db: Session) -> List[models.NodeComments]:
    return db.query(models.NodeComments).all()

#get like all
async def get_object_likes(db: Session) -> List[models.AssetLikes]:
    return db.query(models.AssetLikes).all()

async def get_node_likes(db: Session) -> List[models.NodeLikes]:
    return db.query(models.NodeLikes).all()

#get save all
async def get_object_saves(db: Session) -> List[models.AssetSaves]:
    return db.query(models.AssetLikes).all()

async def get_node_saves(db: Session) -> List[models.NodeSaves]:
    return db.query(models.NodeSaves).all()


#get one comment
async def get_object_comment_by_id(db: Session, id: int):
    return db.query(models.AssetComments).filter(models.AssetComments.id == id).first()

async def get_node_comment_by_id(db: Session, id: int):
    return db.query(models.NodeComments).filter(models.NodeComments.id == id).first()

#update comment
async def object_comment_update(db: Session, id: int, user_id: int, comment: schemas.ObjectCommentUpdate) -> schemas.ObjectCommentReturn:
    db_comment = await get_object_comment_by_id(db, id)
    if not db_comment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    
    if db_comment.user_id != user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You are not comment owner")
    
    update_data = comment.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_comment, key, value)

async def node_comment_update(db: Session, id: int, user_id: int, comment: schemas.NodeCommentUpdate) -> schemas.NodeCommentReturn:
    db_comment = await get_node_comment_by_id(db, id)
    if not db_comment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    
    if db_comment.user_id != user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You are not comment owner")
    
    update_data = comment.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_comment, key, value)


#delete comment
async def object_comment_delete(db: Session, id: int) -> models.AssetComments:
    comment = await get_asset_by_id(db, id)
    if not comment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    db.delete(comment)
    db.commit()
    return comment

async def node_comment_delete(db: Session, id: int) -> models.NodeComments:
    comment = await get_node_by_id(db, id)
    if not comment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    db.delete(comment)
    db.commit()
    return comment

#delete like
async def object_like_delete(db: Session, id: int) -> models.AssetLikes:
    like = await get_asset_by_id(db, id)
    if not like:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    db.delete(like)
    db.commit()
    return like

async def node_like_delete(db: Session, id: int) -> models.NodeLikes:
    like = await get_node_by_id(db, id)
    if not like:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    db.delete(like)
    db.commit()
    return like

#delete save
async def object_save_delete(db: Session, id: int) -> models.AssetSaves:
    save = await get_asset_by_id(db, id)
    if not save:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    db.delete(save)
    db.commit()
    return save

async def node_save_delete(db: Session, id: int) -> models.NodeSaves:
    save = await get_node_by_id(db, id)
    if not save:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    db.delete(save)
    db.commit()
    return save

#follow
async def get_follow_list(db: Session, user_id) -> List[models.FollowFriend]:
    return db.query(models.FollowFriend).filter(user_id == user_id).all()

async def follow_user(db: Session, follow: schemas.FollowUser):
    follow = models.FollowFriend(
        **follow.dict()
    )
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow

#user_profile

async def get_user_profile(db: Session, id: int):
    return db.query(models.User).filter(models.User.user_id == id).first()

async def get_my_profile(db: Session, user_id):
    return db.query(models.User).filter(user_id == user_id).first()