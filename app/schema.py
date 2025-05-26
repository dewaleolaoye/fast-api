from datetime import datetime
from typing import Union
from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    access_token: Union[str, None]

class PublicUserResponse(BaseModel):
    id: int
    email: str
    username: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: PublicUserResponse

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginAuth(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    data: UserResponse
    status: int
    token_type: str

class TokenData(BaseModel):
    id: Union[str, None]
