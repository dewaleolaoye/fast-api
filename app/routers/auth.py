from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import error
from app.database import get_db
from app.oauth2 import create_access_token
from app.utility import find_user_by_username, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post('/login', status_code=status.HTTP_200_OK)
def login(payload:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
# def login(payload:schema.LoginAuth, db:Session=Depends(get_db)):
    user = find_user_by_username(payload.username, db)

    if user is None:
        return error.raise_not_found(id=None, detail="Invalid credentials")

    if not verify_password(payload.password, user.password):
        return error.raise_not_found(id=None, detail="Invalid credentials")
 

    token = create_access_token(data={
        "id": user.id,
        "username": user.username
    })

    return {
        "data": {
            "id": user.id,
            "access_token": token,
            "username": user.username,
            "email": user.email
        },
        "status": status.HTTP_200_OK
    }
