from fastapi import Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt.exceptions import InvalidTokenError

from app import models
from app.database import get_db
from .data import all_posts


def find_post(post_id: int):
    find_post = (post for post in all_posts if post["id"] == post_id)
    post = next(find_post, None)

    return post

    # for post in all_posts:
    #     if post["id"] == post_id:
    #         return post

def find_post_index(id: int):
    for i, p in enumerate(all_posts):
        if p['id'] == id:
            return i
        

def find_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    
    return user

def find_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    return user

def find_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    return user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    return post

