from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class MyBase(BaseModel):
    id:int
    name:str
    created:datetime

class UserBase(MyBase):
    card_id:int
    role_id:int
    email:EmailStr
    active:int
    comments:str
    class Config():
        from_attributes = True


class LoginBase(BaseModel):
    email:EmailStr
    class Config:
        from_attributes = True

class UserLogin(LoginBase):
    password:str

class LoginResponse(LoginBase):
    passwordHash:str

class Roles(MyBase):
    description:str
    class Config():
        from_attributes =True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserCreateOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config():
        from_attributes =True

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str] = None
       