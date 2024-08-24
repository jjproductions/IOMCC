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
    return {"message": "Hello World"}


@app.get("/gettypes")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Type_DB).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no types exist")

    #print(posts)
    return {"data": posts}


# title str, content str, published bool
@app.post("/posts", response_model=schemas.UserBase)
def get_posts(my_posts: schemas.UserBase, db: Session = Depends(get_db)):
    new_post = models.UserAuth_DB(**my_posts.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    print(new_post)
    #print(new_post.model_dump())
    conn.commit()
    #if my_posts == None:
     #   raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="post call requires a json body")

    return {"data": new_post}

@app.put("/posts/{id}", response_model=schemas.UserBase)
def update_post(id:int, post: Post):
    cursor.execute(""" UPDATE "Products" SET name=%s, price=%s, inventory=%s, is_sale=%s WHERE id = %s 
                   RETURNING *""", (post.name, post.price, post.inventory, post.sale, id))
    updated_post = cursor.fetchone()

    

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid id: {id}")
    else:
        conn.commit()
    return {"data": updated_post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute(""" DELETE FROM "Products" WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid id: {id}")
    else:
        conn.commit()
    
    return{status.HTTP_204_NO_CONTENT}




