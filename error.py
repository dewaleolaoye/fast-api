from fastapi import HTTPException, status

def raise_not_found (id: int):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id {id} not found")

def invalid_post(id: int):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid post ID: {id}. Must be a number")