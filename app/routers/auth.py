from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import error, models, schema
from app.database import get_db
from app.oauth2 import create_access_token
from app.utility import find_user_by_email, find_user_by_username, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post('/login', status_code=status.HTTP_200_OK, response_model=schema.Token)
def login(payload:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
# def login(payload:schema.LoginAuth, db:Session=Depends(get_db)):
    user = find_user_by_username(payload.username, db)

    if user is None:
        return error.forbidden("Invalid credentials")

    if not verify_password(payload.password, user.password):
        return error.forbidden("Invalid credentials")
 

    token = create_access_token(data={
        "id": user.id,
        "username": user.username
    })

    return {
        "data": {
            "id": user.id,
            "access_token": token,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at
        },
        "status": status.HTTP_200_OK,
        "token_type": "Bearer"
    }



@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    user_exist = find_user_by_username(user.username, db) or find_user_by_email(user.email, db)

    print(user_exist, 'IT EXIST')
    if user_exist is not None:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "msg": "User already exist",
                "status": status.HTTP_409_CONFLICT
            }
        )

    hashed_password = hash(user.password)
    
    user.password = hashed_password
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(data={
        "id": new_user.id,
        "username": new_user.username
    })

    user_response = {
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username,
        "created_at": new_user.created_at,
        "access_token": token,
    }

    return user_response
