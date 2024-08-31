from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from ..db import get_db
from sqlalchemy.orm import Session
from .. import models,schemas, utils, oauth2


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

#, current_user: int = Depends(oauth2.get_current_user)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(post: schemas.UserCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)) -> schemas.UserCreateOut:
    unauth_exception =  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized for this action", headers={"WWW-Authenticate":"Bearer"})
    #print (f"Created by: {current_user}")
    #if not current_user:
     #   raise unauth_exception
    #validate if your authorized 
    #if not oauth2.is_authorized(data={"role":1,"email":current_user}):
     #   raise unauth_exception
    


    db_user = models.Users_DB(**post.model_dump(exclude={'password'}))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    hashed_password = utils.hash(post.password)

    print(f"user id: {db_user.id} pw hashed: {hashed_password}")
    db_user_auth = models.UserAuth_DB(password=hashed_password, user_id=db_user.id)
    #db_user_auth = schemas.UserAuth(password=hashed_password, user_id=db_user.id)
    print(db_user_auth)
    #db.add(db_user_auth.model_dump())
    db.add(db_user_auth)
    db.commit()
    db.refresh(db_user_auth)
    print(db_user_auth)
    
    return db_user_auth
    #return {"post":"create users"}

@router.get("/")
def get_users(db: Session = Depends(get_db)) -> list[schemas.UserBase]:
    users:schemas.UserBase = db.query(models.Users_DB).all()
    return users

#Test method to get the pw Hash
@router.get("/{pw}")
def get_hash(pw:str):
    pHash = utils.hash(pw)
    #print (pHash)
    return {"hash":pHash}