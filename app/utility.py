from fastapi import Depends
from sqlalchemy.orm import Session
import bcrypt

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

def hash_password(password: str):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password=pwd_bytes, salt=salt)

    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(password=pwd_bytes, hashed_password=hashed_bytes)

def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    return post

