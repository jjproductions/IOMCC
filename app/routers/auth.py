from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .. import db, models, utils, oauth2
from ..config import settings
from sqlalchemy.orm import Session
from typing import Annotated


router = APIRouter(
    prefix="/login",
    tags=['Authentication']
    )

@router.post('/')
async def login(user_credentials:Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(db.get_db)):
    #user = db.query(models.UserAuth_DB).filter(models.UserAuth_DB.email == user_credentials.username).first()
    
    print(f"{user_credentials.username} {user_credentials.password}")
    user = db.query(
        models.Users_DB.id, 
        models.Users_DB.name,
        models.Users_DB.role_id.label("roleId"),
        models.Users_DB.email,
        models.Users_DB.active.label("isActive"),
        models.UserAuth_DB.password.label("pwHash")).join(models.UserAuth_DB, models.UserAuth_DB.user_id == models.Users_DB.id).filter(
        models.Users_DB.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    #print(user.email)
    if not utils.verify(user_credentials.password, user.pwHash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_min)
    access_token = oauth2.create_access_token(sub={"sub":user.email}, expires_delta=access_token_expires)

    return{"access_token":access_token, "token_type":"bearer"}
    #return {"name":"me"}
