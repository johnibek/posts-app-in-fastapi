from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# User
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True




# Post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True




# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None



# Vote
class Vote(BaseModel):
    post_id: int
    dir: int = Field(le=1, ge=0)  # Vote direction of 1 means we want to add a vote, a direction of 0 means we want to delete a vote. 0 <= dir <= 1
