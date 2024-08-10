import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from . import schemas, models
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials.", headers={"WWW-Authenticate": "Bearer"})

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    
    return user


