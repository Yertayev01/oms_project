from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime
import typing as t


class Token(BaseModel):
    user_id: int
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class User(BaseModel):
    user_id: int
    email: str
    socialKind: str
    name: str
    gender: str
    level: int
    self_intro: str
    # profile_images_path: str
    # profile_image_name: str
    
#profile image
class PhotoCreate(BaseModel):
    #user_id: int
    photo_url: str

class PhotoReturn(BaseModel):
    id: int
    user_id: int
    photo_url: str
    reg_dt: datetime
    mod_dt: datetime
    
    class ConfigDict:
        from_attributes = True
#user
class UserBase(BaseModel):
    username: str
    is_admin: t.Optional[bool] = False
  
class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    socialKind: str
    phone_number: int
    latitude: str
    longitude: str
    self_intro: Optional[str] = None
    #photos: PhotoReturn

    
class UserAdminCreate(BaseModel):
    username: str
    password: str
    is_admin: t.Optional[bool] = False

class UserReturn(BaseModel):
    user_id: int
    username: str
    is_admin: t.Optional[bool] = False

    class ConfigDict:
        from_attributes = True

class UserProfileReturn(BaseModel):
    user_id: int
    username: str
    self_intro: str

    class ConfigDict:
        from_attributes = True
    
class UserUpdate(UserBase):
    username: str
    password: t.Optional[str] = None

class UserAdminUpdate(UserBase):
    username: str
    is_admin: t.Optional[bool] = False
    password: t.Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

#object
class ObjectList(BaseModel):
    id: int
    object_title: str
    object_description: str
    # save like comment count

class Object(BaseModel):
    id: int
    object_title: str
    object_description: str

#anchor
class AnchorList(BaseModel):
    anchor_title: str
    latitude: str
    longitude: str

class AnchorNearByMe(BaseModel):
    anchor_title: str
    latitude: str
    longitude: str

#video
class VideoReturn(BaseModel):
    id: int
    user_id: int
    video_title: str
    reg_dt: datetime
    mod_dt: datetime
    #path
    
    class ConfigDict:
        from_attributes = True


#comment
class ObjectCommentCreate(BaseModel):
    object_id: int
    comment: str

class ObjectCommentReturn(BaseModel):
    id: int
    object_id: int
    owner_id: int
    comment: str
    reg_dt: datetime
    mod_dt: datetime

    class ConfigDict:
        from_attributes = True


class NodeCommentCreate(BaseModel):
    node_id: int
    comment: str

class NodeCommentReturn(BaseModel):
    id: int
    node_id: int
    owner_id: int
    comment: str
    reg_dt: datetime
    mod_dt: datetime

    class ConfigDict:
        from_attributes = True

#like
class ObjectLikeCreate(BaseModel):
    object_id: int

class ObjectLikeReturn(BaseModel):
    id: int
    object_id: int
    owner_id: int
    reg_dt: datetime
    mod_dt: datetime

    class ConfigDict:
        from_attributes = True

class NodeLikeCreate(BaseModel):
    node_id: int

class NodeLikeReturn(BaseModel):
    id: int
    node_id: int
    owner_id: int
    reg_dt: datetime
    mod_dt: datetime

    class ConfigDict:
        from_attributes = True

# save
class ObjectSaveCreate(BaseModel):
    object_id: int

class ObjectSaveReturn(BaseModel):
    id: int
    object_id: int
    owner_id: int
    reg_dt: datetime
    mod_dt: datetime

    class ConfigDict:
        from_attributes = True

class NodeSaveCreate(BaseModel):
    node_id: int

class NodeSaveReturn(BaseModel):
    id: int
    node_id: int
    owner_id: int
    reg_dt: datetime
    mod_dt: datetime

    class ConfigDict:
        from_attributes = True

#update
class ObjectCommentUpdate(BaseModel):
    comment: str

class NodeCommentUpdate(BaseModel):
    comment: str

    
#object
class ObjectUpdate(BaseModel):
    object_title: t.Optional[str] = None
    object_description: t.Optional[str] = None


class ObjectsReturn(BaseModel):
    id: int
    user_id: int
    object_type: str
    object_title: str
    object_description: str
    
    class ConfigDict:
        from_attributes = True

class ObjectReturn(BaseModel):
    id: int
    user_id: int
    object_type: str
    object_title: str
    object_description: str
    reg_dt: datetime
    mod_dt: datetime
    comments: t.List[ObjectCommentReturn]
    
    class ConfigDict:
        from_attributes = True


#node
class NodeUpdate(BaseModel):
    node_title: t.Optional[str] = None
    node_description: t.Optional[str] = None


class NodesReturn(BaseModel):
    id: int
    user_id: int
    object_id: int
    node_title: str
    node_description: str
    latitude: str
    longitude: str

    class ConfigDict:
        from_attributes = True

class NodeReturn(BaseModel):
    id: int
    user_id: int
    object_id: int
    node_title: str
    node_description: str
    latitude: str
    longitude: str
    reg_dt: datetime
    mod_dt: datetime
    #comments: t.List[NodeCommentReturn]
    json_file: bytes

    class ConfigDict:
        from_attributes = True

#follow
class FollowList(BaseModel):
    user_id: int
    follower_id: int

class FollowUser(BaseModel):
    user_id: int
    follower_id: int

class FollowReturn(BaseModel):
    user_id: int
    follow_id: int
    reg_dt: datetime
    mod_dt: datetime