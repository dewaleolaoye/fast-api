from typing import Optional
from fastapi import HTTPException, status

def raise_not_found (id: int, detail: Optional[str] = None):
    msg = detail if detail else f"{id} not found"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
        "msg": msg,
        "status": status.HTTP_404_NOT_FOUND
    })

def invalid_post(id: int):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid post ID: {id}. Must be a number")