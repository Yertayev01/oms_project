from sqlalchemy import Column, Integer,  String, ForeignKey, DateTime, Boolean, BigInteger, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable = False, index=True)
    
    email = Column(String(256), unique=True, nullable=False, index=True)
    username = Column(String(256), unique=True, nullable=False)
    password=Column(String(256), nullable=False) 
    socialKind = Column(String(256), nullable=False)
    #firebase_token = Column(String(256), nullable=False)
    phone_number = Column(BigInteger, nullable=False)
    self_intro = Column(String(256), nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    login_dt = Column(DateTime, server_default=func.now())
    reg_dt = Column(DateTime, server_default=func.now())  
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

    payment_dt = Column(DateTime, default=None)
    payment_status = Column(String(256), unique=False, default=False)
    
    # profile_images_path = Column(String(256), nullable=True)
    # profile_image_name = Column(String(256), nullable=True)

    #ANCHOR WORLD relationships
    nodes = relationship("Node", cascade="all,delete", back_populates="owner")
    objects = relationship("Object", cascade="all,delete", back_populates="owner")

    n_comments = relationship("NodeComment", cascade="all,delete", back_populates="owner")
    n_saves = relationship("NodeSave", cascade="all,delete", back_populates="owner")
    n_likes = relationship("NodeLike", cascade="all,delete", back_populates="owner")

    o_comments = relationship("ObjectComment", cascade="all,delete", back_populates="owner")
    o_saves = relationship("ObjectSave", cascade="all,delete", back_populates="owner")
    o_likes = relationship("ObjectLike", cascade="all,delete", back_populates="owner")

    photos = relationship("Photo", cascade="all,delete", back_populates="photo")


    #PIXEL2POLY relationships
    # Asset table in P2P become Object table
    #assets = relationship("Asset", cascade="all,delete", back_populates="owner")
    objectsfiles = relationship("ObjectFile", cascade="all,delete", back_populates="owner")
    fileUploads = relationship("FileUpload", cascade="all,delete", back_populates="owner")

    def __str__(self):
        return self.username
    
class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    photo_url = Column(String, nullable=False)
    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

    photo = relationship("User", back_populates="photos")

    def __str__(self):
        return f"Photo(id={self.id}, post_id={self.user_id}, created_at={self.reg_dt})"

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, nullable = False, index=True)
    
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    owner = relationship("User", cascade="all,delete", back_populates="nodes")

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    #anchor_id = Column(String(256), nullable=False) 
    # anchor_id = Column(Integer, ForeignKey("anchors.id", ondelete="CASCADE"))
    # parentAnchor = relationship("Anchor", back_populates="nodes")

    object_id = Column(String(256), nullable=False) 
    # object_id = Column(Integer, ForeignKey("objects.id", ondelete="CASCADE"))
    # parentObject = relationship("Object", back_populates="nodes")

    node_title = Column(String(256), nullable=False)
    node_description = Column(String(256), nullable=True)
    status = Column(String(256), nullable=False)
    node_json_path = Column(String(256), nullable=False)
    node_json_name = Column(String(256), nullable=False)

    #anchors = relationship("Anchor", cascade="all,delete", back_populates="parent")
    #objects = relationship("Object", cascade="all,delete", back_populates="parent")
    videos = relationship("Video", cascade="all,delete", back_populates="parent")

    jsons = relationship("Json", cascade="all,delete", back_populates="json")

    #titles = relationship("NodeTitle", cascade="all,delete", back_populates="parent")
    #tags = relationship("NodeTag", cascade="all,delete", back_populates="parent")
    comments = relationship("NodeComment", cascade="all,delete", back_populates="parent")
    saves = relationship("NodeSave", cascade="all,delete", back_populates="parent")
    likes = relationship("NodeLike", cascade="all,delete", back_populates="parent")

    
    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Json(Base):
    __tablename__ = 'jsons'

    id = Column(Integer, primary_key=True)
    node_id = Column(Integer, ForeignKey('nodes.id', ondelete="CASCADE"), nullable=False)
    json_url = Column(String, nullable=False)
    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

    json = relationship("Node", back_populates="jsons")

    def __str__(self):
        return f"Json(id={self.id}, json_id={self.node_id}, created_at={self.reg_dt})"

class Anchor(Base):
    __tablename__ = "anchors"

    id = Column(Integer, primary_key=True, nullable = False, index=True)
    #does it have relation with user?
    # node_id = Column(Integer, ForeignKey("nodes.id", ondelete="CASCADE"))
    # parent = relationship("Node", back_populates="anchors")
   
    #nodes = relationship("Node", cascade="all,delete", back_populates="parentAnchor")

    anchor_title = Column(String(256), nullable=False)
    status = Column(String(256), nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Object(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, nullable = False, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="objects")

    #nodes = relationship("Node", cascade="all,delete", back_populates="parentObject")

    
    # node_id = Column(Integer, ForeignKey("nodes.id", ondelete="CASCADE"))
    # parent = relationship("Node", back_populates="objects")

    likes = relationship("ObjectLike", cascade="all,delete", back_populates="parent")
    comments = relationship("ObjectComment", cascade="all,delete", back_populates="parent")
    saves = relationship("ObjectSave", cascade="all,delete", back_populates="parent")
    #tags = relationship("ObjectTag", cascade="all,delete", back_populates="parent")
    object_files = relationship("ObjectFile", cascade="delete", back_populates="object")
    #titles = relationship("ObjectTitle", cascade="all,delete", back_populates="parent")

    object_title = Column(String(256), nullable=False)
    object_description = Column(String(256), nullable=True)
    
    object_type = Column(String(256), nullable=False)
    #file_ext = Column(String(256), nullable=False)
    status = Column(String(256), nullable=False)
    conversion_status = Column(String(10), default=0)
    #conversion_type = Column(String(10), nullable=True)

    object_uuid = Column(String(256), nullable=False)
    object_file_path = Column(String(256), nullable=True)
    object_file_name = Column(String(256), nullable=True)
    object_thumb_name = Column(String(256), nullable=True)

    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

class ObjectFile(Base):
    __tablename__ = "objectfiles"
    
    id = Column(Integer, primary_key=True, nullable=False)
    object_file_id = Column(Integer, ForeignKey("objects.id", ondelete="CASCADE"))

    object_file_name = Column(String(256), nullable=False)
    object_file_uuid = Column(String(256), nullable=False)    
    object_file_count = Column(Integer, nullable=False)
    object_file_type = Column(String(256), nullable=False) 
    object_file_path = Column(String(256), nullable=False)
    asset_file_reg_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())
    asset_file_mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="objectsfiles")

    object = relationship("Object", back_populates="object_files")

    def return_pth(self):
        return self.object_file_path, self.object_file_name

class FileUpload(Base):
    __tablename__ = "fileUploads"

    fileUpload_id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    fileUpload_uuid = Column(String(256), nullable=False)
    fileUpload_path = Column(String(256), nullable=False)
    fileUpload_filename = Column(String(256), nullable=False)
    fileUpload_file_count = Column(Integer, nullable=False)  
    fileUpload_status = Column(String(256), nullable=False)
    fileUpload_conversion_type = Column(String(256), nullable=False)
    fileUpload_reg_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())
    fileUpload_mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

    owner_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=True)    
    owner = relationship("User", back_populates="fileUploads")

class Video(Base):
    __tablename__  = "videos"

    id = Column(Integer, primary_key=True, nullable = False, index=True)

    node_id = Column(Integer, ForeignKey("nodes.id", ondelete="CASCADE"))
    parent = relationship("Node", back_populates="videos")
   
    video_title = Column(String(256), nullable=False)
    video_uuid = Column(String(256), nullable=False)
    video_file_path = Column(String(256), nullable=False)
    video_file_name = Column(String(256), nullable=False)
    video_thumb_name = Column(String(256), nullable=True)

    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

class NodeTag(Base):
    __tablename__ = "node_tags"

    id = Column(Integer, primary_key=True, nullable = False, index=True)

    node_id = Column(String(256), nullable=False)
    # node_id = Column(Integer, ForeignKey("nodes.id", ondelete="CASCADE"))
    # parent = relationship("Node", back_populates="tags")

    tag = Column(String(256), nullable=False)

    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

class ObjectTag(Base):
    __tablename__ = "obj_tags"

    id = Column(Integer, primary_key=True, nullable = False, index=True)

    object_id = Column(String(256), nullable=False)
    # object_id = Column(Integer, ForeignKey("objects.id", ondelete="CASCADE"))
    # parent = relationship("Object", back_populates="tags")

    tag = Column(String(256), nullable=False)

    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

class NodeComment(Base):
    __tablename__ = "node_comments"

    id = Column(Integer, primary_key=True, nullable = False, index=True)

    node_id = Column(Integer, ForeignKey("nodes.id", ondelete="CASCADE"))
    parent = relationship("Node", back_populates="comments")

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="n_comments")
    
    comment = Column(String(256), nullable=False)

    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

class ObjectComment(Base):
    __tablename__ = "obj_comments"

    id = Column(Integer, primary_key=True, nullable = False, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="o_comments")

    object_id = Column(Integer, ForeignKey("objects.id", ondelete="CASCADE"))
    parent = relationship("Object", back_populates="comments")
    

    comment = Column(String(256), nullable=False)

    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

class NodeSave(Base):
    __tablename__ = "node_saves"

    id = Column(Integer, primary_key=True, nullable = False, index=True)

    node_id = Column(Integer, ForeignKey("nodes.id", ondelete="CASCADE"))
    parent = relationship("Node", back_populates="saves")

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="n_saves")

    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

class ObjectSave(Base):
    __tablename__ = "obj_saves"

    id = Column(Integer, primary_key=True, nullable = False, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="o_saves")

    object_id = Column(Integer, ForeignKey("objects.id", ondelete="CASCADE"))
    parent = relationship("Object", back_populates="saves")

    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

class NodeLike(Base):
    __tablename__ = "node_likes"

    id = Column(Integer, primary_key=True, nullable = False, index=True)

    node_id = Column(Integer, ForeignKey("nodes.id", ondelete="CASCADE"))
    parent = relationship("Node", back_populates="likes")

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="n_likes")

    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

class ObjectLike(Base):
    __tablename__ = "obj_likes"

    id = Column(Integer, primary_key=True, nullable = False, index=True)

    object_id = Column(Integer, ForeignKey("objects.id", ondelete="CASCADE"))
    parent = relationship("Object", back_populates="likes")

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="o_likes")

    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, nullable = False, index=True)

    user_id = Column(Integer, unique=False, nullable=True)
    follower_id = Column(Integer, unique=False, nullable=True)

    reg_dt = Column(DateTime, server_default=func.now()) 
    mod_dt = Column(DateTime, server_default=func.now(), onupdate=func.now())






