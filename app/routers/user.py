from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..utils import hash_password
from .. import models
from ..database import get_db
from ..schemas import UserIn, UserOut

router = APIRouter(prefix="/users", tags=['users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register_user(user: UserIn, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{user_id}", status_code=200, response_model=UserOut)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no user with this id.")

    return user


@router.get("/", status_code=200, response_model=list[UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users