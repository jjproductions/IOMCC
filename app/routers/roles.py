from fastapi import APIRouter, Depends
from ..db import get_db
from sqlalchemy.orm import Session
from .. import models,schemas

router = APIRouter(
    prefix="/roles",
    tags=['Roles']
)

@router.get("/")
async def get_roles(db: Session = Depends(get_db)):
    posts = db.query(models.Role_DB).all()
    return posts