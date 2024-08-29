from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class MyBase(BaseModel):
    id:int
    name:str
    created_at:datetime

class UserBase(MyBase):
    card_id:int | None
    role_id:int
    email:EmailStr
    active:int
    comments:str | None
    class Config():
        from_attributes = True


class LoginBase(BaseModel):
    email:EmailStr
    class Config:
        from_attributes = True

class UserLogin(LoginBase):
    password:str
    email:EmailStr

class LoginResponse(LoginBase):
    passwordHash:str

class Roles(MyBase):
    description:str
    class Config():
        from_attributes =True

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    name:str
    role_id:int
    class Config():
        from_attributes = True
class UserCreateOut(BaseModel):
    id:int
    created_at:datetime
    class Config():
        from_attributes = True

class UsersDisplay(UserBase):
    email:EmailStr

class UserAuth(BaseModel):
    user_id:int
    password:str

    class Config():
        from_attributes = True

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str] = None

class TokenRoleData(BaseModel):
    role:Optional[str] = None
       