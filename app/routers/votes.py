from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, database, oauth2, models
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def make_vote(vote: schemas.MakeVoting, db: Session = Depends(database.get_db), 
current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist"
        )

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code= status.HTTP_409_CONFLICT,
                detail= f"Vote already exist with voter id {current_user.id}"
            )

        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message": "Successfully aded vote"}   

    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Vote does not exists")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}    

