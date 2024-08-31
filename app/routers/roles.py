from fastapi import APIRouter, Depends
from ..db import get_db
from sqlalchemy.orm import Session
from .. import models,schemas, oauth2

router = APIRouter(
    prefix="/roles",
    tags=['Roles']
)

@router.get("/")
async def get_roles(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    posts = db.query(models.Role_DB).all()
    return posts