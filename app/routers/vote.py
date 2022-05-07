from fastapi import FastAPI, Body, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, schema, oauth2
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user.uid)
    found_vote = vote_query.first()


    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{vote.post_id} post is not found.")

    #Vote
    if(vote.dir == 1):
        #If Vote is found and User wants to like again, Throw Exception
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User{user.uid} has already voted on this post.")
        #Add Vote to database
        new_vote = models.Vote(post_id=vote.post_id, user_id=user.uid)
        db.add(new_vote)
        db.commit()
        return {"message": "Sucessfully added vote."}
    #Unvote
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist.")

        vote_query.delete(synchronize_session= False)
        db.commit()

        return{"message": "Post Unvoted."}
