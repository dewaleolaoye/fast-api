from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import schema
from app.database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post('/login', status_code=status.HTTP_201_CREATED)
def login(payload:schema.LoginAuth, db:Session=Depends(get_db)):

    return ""