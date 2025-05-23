from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, status

from .database import engine, get_db
from . import models, schema, error

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
        
    return {
        "data": posts,
        "msg": "successfully fetched data"
    }


@app.post('/createposts', status_code=status.HTTP_201_CREATED)
def create_post(payload: schema.PostCreate, db: Session = Depends(get_db)): 
    new_post = models.Post(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "data": new_post,
        "msg": "successfully create new post"
    }
    

@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)): 
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        error.raise_not_found(id)

    return {
        "data": post
    } 


@app.delete('/posts/{id}', status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        error.raise_not_found(id)

    post.delete(synchronize_session=False)
    db.commit()

    return {
        "msg": f"Post {id} deleted successfully",
    }


@app.put('/posts/{id}')
def update_post(id:int, payload:schema.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post is None:
        error.raise_not_found(id)

    post_query.update(payload.model_dump(), synchronize_session=False)
    db.commit()
    
    return {
        "msg": "Post updated successfully ",
        "data": post_query.first()
    }
