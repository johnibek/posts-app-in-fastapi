from fastapi import status, APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
from ..database import get_db
from ..schemas import PostUpdate, PostCreate, PostResponse, UserOut, PostOut
from .. import oauth2


router = APIRouter(prefix="/posts", tags=['posts'], dependencies=[Depends(oauth2.get_current_user)])


@router.get("/", response_model=list[PostOut])
async def get_posts(
        db: Session = Depends(get_db),
        current_user: UserOut = Depends(oauth2.get_current_user),
        limit: int = 5,
        skip: int = 0,
        search: str | None = ""):

    # The below code allows user to get posts only that user has created
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()

    posts = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).
             join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).
             group_by(models.Post.id).filter(models.Post.title.icontains(search)).
             limit(limit).
             offset(skip).all())

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.model_dump(), user_id=current_user.id)  # title=post.title, content=post.content, published=post.published
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{post_id}", response_model=PostOut)
async def get_post(post_id: int, db: Session = Depends(get_db), current_user: UserOut = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == post_id).first()

    post = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).
             join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).
             group_by(models.Post.id).filter(models.Post.id == post_id)).first()

    if not post:
        raise HTTPException(status_code=404, detail="There is no post with this id.")

    if post.Post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    return post



@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no post with this id")

    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", status_code=200, response_model=PostResponse)
async def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no post with this id.')
    
    if post_query.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
