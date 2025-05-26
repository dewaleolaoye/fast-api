
from typing import List
from fastapi import APIRouter, Depends, status
from app import error, models, schema
from app.database import get_db
from sqlalchemy.orm import Session

from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[schema.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
        
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(payload: schema.PostCreate, db: Session = Depends(get_db)): 
    # print(user_id, 'USER ID HERE')
    new_post = models.Post(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

@router.get('/{id}', response_model=schema.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)): 
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
       return error.raise_not_found(id)

    return post


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        return error.raise_not_found(id)

    post.delete(synchronize_session=False)
    db.commit()

    return {
        "msg": f"Post {id} deleted successfully",
    }


@router.put('/{id}', response_model=schema.PostResponse)
def update_post(id:int, payload:schema.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post is None:
        return error.raise_not_found(id)

    post_query.update(payload.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()