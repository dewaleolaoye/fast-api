from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from app import error, models, schema
from app.database import get_db
from sqlalchemy.orm import Session

from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(get_current_user)]
)

# @router.get("/")
@router.get("/", response_model=List[schema.PostWithVotes])
def get_posts(db: Session = Depends(get_db), limit:int= 10, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
    .group_by(models.Post.id)\
    .all()

    return posts


@router.get("/user", response_model=List[schema.PostResponse])
def get_posts_by_user(db: Session = Depends(get_db), user: schema.UserResponse = Depends(get_current_user)):
    posts = db.query(models.Post).filter(models.Post.user_id == user.id).all()
        
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(payload: schema.PostCreate, db: Session = Depends(get_db), user: schema.UserResponse = Depends(get_current_user)): 
    # update_payload = payload.model_copy(update={"user_id": user.id})
    
    new_post = models.Post(user_id=user.id, **payload.model_dump())
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
def delete_post(id: int, db: Session = Depends(get_db), user: schema.UserResponse = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        return error.raise_not_found(id)
    
    if (user.id != post.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can not perform this operation")
        

    post_query.delete(synchronize_session=False)
    db.commit()

    return {
        "msg": f"Post {id} deleted successfully",
    }


@router.put('/{id}', response_model=schema.PostResponse)
def update_post(id:int, payload:schema.PostCreate, db: Session = Depends(get_db), user: schema.UserResponse = Depends(get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post is None:
        return error.raise_not_found(id)
    
    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can not perform this operation") 

    post_query.update(payload.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()