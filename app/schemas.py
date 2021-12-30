from datetime import datetime
from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import List


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


class User_resp(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class resp(BaseModel):
    id: int
    title: str
    content: str
    created: datetime
    url_type: str
    image_url: str
    user: User_resp

    class Config:
        orm_mode = True


class Post_Resp(BaseModel):
    id: int
    title: str
    content: str
    created: datetime

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    posts: List[Post_Resp]

    class Config:
        orm_mode = True


class updat(BaseModel):
    username: str
    email: EmailStr


class post1(BaseModel):
    title: str
    content: str
    url_type: str
    image_url: str


class Authorize(BaseModel):
    email: EmailStr
    password: str
