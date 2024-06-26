from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class postCreate(PostBase):  
    pass    


class CreateUserResponse(BaseModel):
    id: int
    email: EmailStr 
    created_at: datetime       

    class Config():
        orm_mode= True



class PostResponse(BaseModel):   #PostBase:
    # valid this way
    #id: int
    #created_at: datetime

    # but for ordering sake i'm going to specify the order i want
    id: int
    title: str
    content: str
    published: bool = True
    owner_id: int
    created_at: datetime
    owner: CreateUserResponse
    

    class Config:
        orm_mode= True

class PostVoteResponse(BaseModel):
    Post: PostResponse
    votes: int


    class Config:
        orm_mode= True


class CreateUser(BaseModel):
    email: EmailStr
    password: str    


class user_login(BaseModel):
    email: EmailStr
    password: str  

class Token(BaseModel):
        access_token : str
        token_type: str

class  TokenData(BaseModel):
    id: Optional[str] = None

class MakeVoting(BaseModel):
    post_id: int
    dir: conint(le=1)
