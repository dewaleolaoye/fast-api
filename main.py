from random import randrange
from typing import Optional, Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: Union[bool, None] = True
    rating: Optional[float] = None

all_posts = [
  {
    "id": 1,
    "title": "Require despite must among quality wide on.",
    "content": "Sometimes follow let situation state second throw where. Else player he top animal how itself.",
    "published": False,
    "rating": 4.8
  },
  {
    "id": 2,
    "title": "Training letter money like.",
    "content": "Address even meet who. Color watch green nothing treatment suffer out might. Stuff chance southern method glass your. Try management style responsibility scene maybe century.",
    "published": True,
    "rating": 4.3
  },
  {
    "id": 3,
    "title": "Will sing reach film or.",
    "content": "Something eight information staff week exactly shake. List into may another decision exactly late. Value song simple sure.",
    "published": True,
    "rating": 3.9
  },
  {
    "id": 4,
    "title": "House since seem consider yard.",
    "content": "Expert part benefit worker.",
    "published": True,
    "rating": 2.3
  },
  {
    "id": 5,
    "title": "Determine put outside explain democratic.",
    "content": "Share up job fight hope both form. Car culture wrong certainly.",
    "published": False,
    "rating": 3.3
  },
  {
    "id": 6,
    "title": "You theory talk action whose wonder move.",
    "content": "Record him put away matter commercial father. Article owner majority old blue mission.",
    "published": False,
    "rating": 1.4
  },
  {
    "id": 7,
    "title": "Although stuff baby run central marriage.",
    "content": "Few along ask best anyone rate. Available purpose improve listen available resource interesting.",
    "published": False,
    "rating": 3.0
  },
  {
    "id": 8,
    "title": "They beyond south.",
    "content": "Quite center he leader free around long.",
    "published": False,
    "rating": 2.6
  },
  {
    "id": 9,
    "title": "Southern answer final.",
    "content": "Pm natural exactly partner capital church too. Arm only detail window since relationship. Recent concern camera dog spring size.",
    "published": True,
    "rating": 3.7
  },
  {
    "id": 10,
    "title": "In forget cost focus.",
    "content": "Make learn interview pay True arm more debate. Identify rock late pressure position smile. Similar line ok require try computer that.",
    "published": True,
    "rating": 3.8
  }
]


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

    post = [post for post in all_posts if post["id"] == int(id)][0] 

    return {
        "data": post
    }