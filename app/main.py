import time
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
import os
import psycopg
from psycopg.rows import dict_row
from . import models, schemas
from .db import engine, get_db
from sqlalchemy.orm import Session
from .routers import users, roles, types, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Routes
app.include_router(roles.router)
app.include_router(users.router)
app.include_router(auth.router)


class Post(BaseModel):
    name: str
    price: float
    sale: Optional[bool] = False
    inventory: Optional[int] = 0

dbConnectAttempts = 5

while dbConnectAttempts > 0:
    try:
        conn = psycopg.connect(host=os.getenv("DB_SERVER"), dbname=os.getenv("DB_IOM_DATABASE"),
                               user=os.getenv("DB_IOM_USER"), password=os.getenv("DB_IOM_PASSWORD"), row_factory=dict_row)
        cursor = conn.cursor()
        print ("Database connection successful")
        break
    except Exception as error:
        print("Connecting to DB failed")
        print("Error: ", error)
        dbConnectAttempts -= 1
        time.sleep(3)
                           

@app.get("/")
def root():
    #print (os.getenv("DB_IOM_USER"))
    return {"message": "The Institute of Music for Children"}







