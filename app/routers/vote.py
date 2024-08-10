from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(prefix="/vote", tags=['vote'])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote_posts(vote: schemas.Vote,
                     db: Session = Depends(database.get_db),
                     current_user: schemas.UserOut = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id of {vote.post_id} does not exist.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} already voted on this post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}


    elif vote.dir == 0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="you did not vote on this post")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'message': 'successfully deleted vote'}

