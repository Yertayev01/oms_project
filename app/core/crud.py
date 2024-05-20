from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core import models, schemas, utils
from sqlalchemy import func
#from app.core.utils import hash_password

#user
async def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.user_id == user_id).first()

async def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()

async def get_users(db: Session) -> List[models.User]:
    return db.query(models.User).all()

async def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()

async def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()

async def user_create(db: Session, user: schemas.UserCreate) -> models.User:
    # Check if email exists
    existing_email = await get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(detail=f"Email {user.email} is already registered", status_code=status.HTTP_409_CONFLICT)

    # Check if username exists
    existing_username = await get_user_by_username(db, user.username)
    if existing_username:
        raise HTTPException(detail=f"Username {user.username} is already taken", status_code=status.HTTP_409_CONFLICT)
    
    user.password = await utils.hash_password(user.password)
    db_user = models.User(
        **user.dict(),
    )
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

#object
async def get_object_by_id(db: Session, id: int):
    return db.query(models.Object).filter(
        models.Object.id == id,
        models.Object.conversion_status == '2'
        ).first()

async def get_objects(db: Session) -> List[models.Object]:
    return db.query(models.Object).filter(models.Object.conversion_status == '2').all()

async def get_only_my_objects(db: Session, user_id: int, object_type: str) -> List[models.Object]:
    return db.query(models.Object).filter(
        models.Object.user_id == user_id,
        models.Object.object_type == object_type,
        models.Object.conversion_status == '2'
    ).all()

async def get_only_user_objects(db: Session, user_id: int, object_type: str) -> List[models.Object]:
    return db.query(models.Object).filter(
        models.Object.object_type == object_type,
        models.Object.conversion_status == '2',
        models.Object.user_id != user_id
    ).all()

async def object_update(db: Session, id: int, user_id: int, object: schemas.ObjectUpdate) -> schemas.ObjectReturn:
    db_object = await get_object_by_id(db, id)
    if not db_object:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if db_object.user_id != user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You are not post owner")
    
    update_data = object.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_object, key, value)

    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object

#node
async def get_node_by_id(db: Session, id: int):
    return db.query(models.Node).filter(models.Node.id == id).first()

async def get_nodes(db: Session) -> List[models.Node]:
    return db.query(models.Node).all()

async def get_only_my_nodes(db: Session, user_id: int) -> List[models.Node]:
    return db.query(models.Node).filter(models.Node.user_id == user_id).all()

async def get_only_user_nodes(db: Session, user_id: int) -> List[models.Node]:
    return db.query(models.Node).filter(models.Node.user_id != user_id).all()

async def node_update(db: Session, id: int, user_id: int, node: schemas.NodeUpdate) -> schemas.NodeReturn:
    db_node = await get_node_by_id(db, id)
    if not db_node:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if db_node.user_id != user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You are not post owner")
    
    update_data = node.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_node, key, value)

    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node



async def get_nodes_on_map(db: Session, latitude: float, longitude: float) -> List[dict]:
    
    import math

    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371000  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    
    nodes = db.query(models.Node).all()
    nodes_with_distance = [
        (node, calculate_distance(latitude, longitude, node.latitude, node.longitude))
        for node in nodes
    ]
    nodes_with_distance.sort(key=lambda x: x[1])
    return [{'node': node, 'distance': distance} for node, distance in nodes_with_distance]

#video

async def get_video_by_id(db: Session, id: int):
    return db.query(models.Video).filter(models.Video.id == id).first()

async def get_videos(db: Session) -> List[models.Video]:
    return db.query(models.Video).all()

async def get_only_my_videos(db: Session, user_id) -> List[models.Video]:
    return db.query(models.Video).join(models.Node, models.Node.id == models.Video.node_id).filter(models.Node.user_id == user_id).all()

async def get_only_user_videos(db: Session, user_id) -> List[models.Video]:
    return db.query(models.Video).join(models.Node, models.Node.id == models.Video.node_id).filter(models.Node.user_id != user_id).all()


async def video_update(db: Session, id: int, user_id: int, video: schemas.VideoUpdate) -> schemas.VideoReturn:
    db_video = await get_video_by_id(db, id)
    if not db_video:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if db_video.user_id != user_id:
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
    comment = models.ObjectComment(
            **comment.dict(), user_id = user_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def post_node_comment(db: Session, comment: schemas.NodeCommentCreate, user_id):
    comment = models.NodeComment(
            **comment.dict(), user_id = user_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

#post like
async def post_object_like(db: Session, like: schemas.ObjectLikeCreate, user_id):
    like = models.ObjectLike(
            **like.dict(), user_id = user_id
    )
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

async def post_node_like(db: Session, like: schemas.NodeLikeCreate, user_id):
    like = models.NodeLike(
            **like.dict(), user_id = user_id
    )
    db.add(like)
    db.commit()
    db.refresh(like)
    return like


#post save
async def post_object_save(db: Session, save: schemas.ObjectSaveCreate, user_id):
    save = models.ObjectSave(
            **save.dict(), user_id = user_id
    )
    db.add(save)
    db.commit()
    db.refresh(save)
    return save

async def post_node_save(db: Session, save: schemas.NodeSaveCreate, user_id):
    save = models.NodeSave(
            **save.dict(), user_id = user_id
    )
    db.add(save)
    db.commit()
    db.refresh(save)
    return save


#get comment all
async def get_object_comments(db: Session) -> List[models.ObjectComment]:
    return db.query(models.ObjectComment).all()

async def get_node_comments(db: Session) -> List[models.NodeComment]:
    return db.query(models.NodeComment).all()

#get like all
async def get_object_likes(db: Session) -> List[models.ObjectLike]:
    return db.query(models.ObjectLike).all()

async def get_node_likes(db: Session) -> List[models.NodeLike]:
    return db.query(models.NodeLike).all()

#get save all
async def get_object_saves(db: Session) -> List[models.ObjectSave]:
    return db.query(models.ObjectLike).all()

async def get_node_saves(db: Session) -> List[models.NodeSave]:
    return db.query(models.NodeSave).all()


#get one comment
async def get_object_comment_by_id(db: Session, id: int):
    return db.query(models.ObjectComment).filter(models.ObjectComment.id == id).first()

async def get_node_comment_by_id(db: Session, id: int):
    return db.query(models.NodeComment).filter(models.NodeComment.id == id).first()

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
async def object_comment_delete(db: Session, id: int) -> models.ObjectComment:
    comment = await get_object_by_id(db, id)
    if not comment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    db.delete(comment)
    db.commit()
    return comment

async def node_comment_delete(db: Session, id: int) -> models.NodeComment:
    comment = await get_node_by_id(db, id)
    if not comment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    db.delete(comment)
    db.commit()
    return comment

#delete like
async def object_like_delete(db: Session, id: int) -> models.ObjectLike:
    like = await get_object_by_id(db, id)
    if not like:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    db.delete(like)
    db.commit()
    return like

async def node_like_delete(db: Session, id: int) -> models.NodeLike:
    like = await get_node_by_id(db, id)
    if not like:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    db.delete(like)
    db.commit()
    return like

#delete save
async def object_save_delete(db: Session, id: int) -> models.ObjectSave:
    save = await get_object_by_id(db, id)
    if not save:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    db.delete(save)
    db.commit()
    return save

async def node_save_delete(db: Session, id: int) -> models.NodeSave:
    save = await get_node_by_id(db, id)
    if not save:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    db.delete(save)
    db.commit()
    return save

#follow
async def get_follow_list(db: Session, user_id) -> List[models.Subscription]:
    return db.query(models.Subscription).filter(user_id == user_id).all()

async def follow_user(db: Session, follow: schemas.FollowUser):
    follow = models.Subscription(
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