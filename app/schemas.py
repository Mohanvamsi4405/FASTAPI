from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional
# Pydantic schema for incoming post data

class UserCreate(BaseModel):
    email: EmailStr
    password:str
    class Config:
        from_attributes = True
        
class UserCreateResponse(BaseModel):
    id: int
    email: EmailStr
    
    
    class Config:
        from_attributes = True

class UserOutputResponse(BaseModel):
    id: int
    email: EmailStr
    
    
    class Config:
        from_attributes = True
        
class Userlogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    token:str
    token_type:str
    

class PostBase(BaseModel):
    content: str
    title: str
    published: bool = True
class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass



    
class TokenData(BaseModel):
    id: Optional[str] = None
    
    
    
    
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner:UserCreateResponse
    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id:int
    dir:conint(le=1) # type: ignore
    
class join(BaseModel):
    pass
    