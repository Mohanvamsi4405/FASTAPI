from .database import Base
from sqlalchemy import Column, ForeignKey , Integer ,Float , String , Boolean ,text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import Relationship



class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean,server_default='TRUE', default=True)
    created_at=Column(TIMESTAMP,server_default=text("NOW()"))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner=Relationship("Users")
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP,server_default=text("NOW()"))
    
    
    
class Votes(Base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)









