from functools import lru_cache
from fastapi import  FastAPI

from app import config
from .database import engine
from . import models
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@lru_cache
def get_settings():
    return config.Settings()

@app.get("/")
def read_root():
    get_settings()
    return {"message": "Hello World"}
