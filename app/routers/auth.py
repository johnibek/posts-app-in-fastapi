from fastapi import APIRouter, status, HTTPException, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
# from ..schemas import UserLogin
from .. import models
from ..utils import verify_password
from ..oauth2 import create_access_token

router = APIRouter(tags=['authentication'], prefix="/users/auth")

# @router.post("/login")
# async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
#
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
#
#     if not verify_password(user_credentials.password, user.password):
#         raise HTTPException(status_code=404, detail="Invalid credentials")
#
#     access_token = create_access_token(data={'user_id': user.id})
#
#     return {'access token': access_token, "token_type": "Bearer"}


@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = create_access_token(data={'user_id': user.id})

    return {'access_token': access_token, "token_type": "Bearer"}
