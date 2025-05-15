from random import randrange
from typing import Optional, Union
from fastapi import FastAPI
from pydantic import BaseModel
from data import all_posts
from error import invalid_post, raise_not_found
from utility import find_post

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: Union[bool, None] = True
    rating: Optional[float] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_posts():
    return {
        "data": all_posts,
        "msg": "successfully fetched data"
    }


@app.post('/createposts')
def create_post(payload: Post):
    new_post = payload.model_dump()

    new_post['id'] = randrange(0, 1000000)

    all_posts.append(new_post)
    return {
        "data": new_post,
        "msg": "successfully create new post"
    }


@app.get('/posts/{id}')
def get_post(id: str): 
      try:
        post = find_post(int(id))
        
      except ValueError:
        invalid_post(id)

      if post is None:
          raise_not_found(id)

      return {
          "data": post
      } 