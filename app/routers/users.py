from fastapi import APIRouter, Depends, status
from ..db import get_db
from sqlalchemy.orm import Session
from .. import models,schemas, utils, oauth2


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(post: schemas.UserCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)) -> schemas.UserCreateOut:
    
    hashed_pwd = utils.hash(post.password)
    post.password = hashed_pwd
    oauth2.get_current_user
    new_post = models.UserAuth_DB(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    return new_post