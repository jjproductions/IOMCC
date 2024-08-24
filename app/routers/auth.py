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
    user = db.query(models.UserAuth_DB).filter(models.UserAuth_DB.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_min)
    access_token = oauth2.create_access_token(sub={"sub":user.id}, expires_delta=access_token_expires)

    return{"access_token":access_token, "token_type":"bearer"}
