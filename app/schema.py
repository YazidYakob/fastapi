from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class UserOut(BaseModel):
    uid: int
    email: EmailStr
    created_on: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    poster_user_id: int
    created_on: datetime
    poster: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    uid: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

