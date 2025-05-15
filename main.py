from random import randrange
from typing import Optional, Union
from fastapi import FastAPI, status
from pydantic import BaseModel
from data import all_posts
from error import raise_not_found
from utility import find_post, find_post_index

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


@app.post('/createposts', status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    new_post = payload.model_dump()

    new_post['id'] = randrange(0, 1000000)

    all_posts.append(new_post)
    return {
        "data": new_post,
        "msg": "successfully create new post"
    }


@app.get('/posts/{id}')
def get_post(id: int): 
      # print(response)
      post = find_post(id)
      # try:
        
      # except ValueError:
      #   invalid_post(id)

      if post is None:
          raise_not_found(id)

      return {
          "data": post
      } 

@app.delete('/posts/{id}', status_code=status.HTTP_200_OK)
def delete_post(id: int):
    index = find_post_index(id)
    
    if index is None:
        raise_not_found(id)

    all_posts.pop(index)

    return {
        "msg": f"Post {id} deleted successfully",
    }

@app.put('/posts/{id}')
def update_post(id:int, updated_post:Post):
    print(updated_post, 'UPDATED POST')
    post_index = find_post_index(id)

    if post_index is None:
        raise_not_found(id)

    post_dict = updated_post.model_dump()
    post_dict['id'] = id

    all_posts[post_index] = post_dict

    return {
        "msg": "Post updated successfully ",
        "data": post_dict
    }