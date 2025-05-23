# from random import randrange
import time
from typing import Union
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, status
import psycopg2
from psycopg2.extras import RealDictCursor

from pydantic import BaseModel

from .database import engine, get_db
from .error import raise_not_found

from . import models

models.Base.metadata.create_all(bind=engine)

def create_db_and_tables():
    models.metadata.create_all(engine)



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: Union[bool, None] = True

while True:

    try:
        conn = psycopg2.connect(
            host="localhost", 
            database="fastapi", 
            user="postgres", 
            password="1234", 
            cursor_factory=RealDictCursor
            )
        
        cur = conn.cursor()
        print("Database connected successfull")

        break
    except Exception as error:
        time.sleep(2)
        print(error, 'CONNECTION FAILED') 


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    
    return {
        "data": posts,
        "msg": "successfully fetched data"
    }


@app.post('/createposts', status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    cur.execute(""" INSERT INTO posts 
                ( title, content, is_published ) VALUES (%s, %s, %s) RETURNING *""", 
                (payload.title, payload.content, payload.published))

    new_post = cur.fetchone()

    conn.commit()
    return {
        "data": new_post,
        "msg": "successfully create new post"
    }


@app.get('/posts/{id}')
def get_post(id: int): 
      cur.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
      post = cur.fetchone()

      if post is None:
          raise_not_found(id)

      return {
          "data": post
      } 

@app.delete('/posts/{id}', status_code=status.HTTP_200_OK)
def delete_post(id: int):
    cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    delete_post = cur.fetchone()
    conn.commit()

    if delete_post is None:
        raise_not_found(id)

    return {
        "msg": f"Post {id} deleted successfully",
        "data": delete_post
    }

@app.put('/posts/{id}')
def update_post(id:int, updated_post:Post):
    
    cur.execute(""" UPDATE posts SET 
                title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *""", 
                (updated_post.title, updated_post.content, updated_post.published, str(id)))
    
    post = cur.fetchone()
    conn.commit()

    if post is None:
        raise_not_found(id)

    return {
        "msg": "Post updated successfully ",
        "data": post
    }


@app.post('/sql')
def test_post(db: Session = Depends(get_db)):
    return {"status": "success"}