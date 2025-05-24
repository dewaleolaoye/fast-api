from typing import List
from fastapi import APIRouter, Depends, status
from app import error, models, schema
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users"
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash(user.password)
    
    user.password = hashed_password
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schema.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        error.raise_not_found(id)

    return user

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schema.UserResponse])
def get_users(db: Session = Depends(get_db)):
    
    user = db.query(models.User).all()

    return user
