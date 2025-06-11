from fastapi import APIRouter, Depends, HTTPException, status
from app import models, schema
from app import oauth2
from app.database import get_db
from sqlalchemy.orm import Session

from app.oauth2 import get_current_user
from app.utility import get_post

router = APIRouter(
    prefix="/vote",
    tags=["Vote"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.VoteModel, user: schema.UserResponse = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    post = get_post(vote.post_id, db)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id)

    found_vote = vote_query.first()
    if (vote.dir == 1):
       if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User has already voted on post {vote.post_id}")
       new_vote = models.Vote(post_id = vote.post_id, user_id = user.id)

       db.add(new_vote)
       db.commit()

       return {
           "message": "Successfully added vote"
       }
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {
            "message": "Successfully deleted vote"
        }
    