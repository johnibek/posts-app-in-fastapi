from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import date
import uvicorn

fake_db = [
    {"id": 1, "title": "title1", 'content': 'content1', 'created_at': date(2023, 3, 2)},
    {'id': 2, 'title': 'title2', 'conetent': 'content2'}
]

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    created_at: date | None = None


def find_post(id):
    for p in fake_db:
        if p['id'] == id:
            return p


def find_post_index(id):
    for i, p in enumerate(fake_db):
        if p['id'] == id:
            return i
        

@app.get("/posts/", tags=['posts'], status_code=status.HTTP_200_OK)
async def get_posts():
    return {"all_posts": fake_db}


@app.get("/posts/{post_id}", tags=['posts'], status_code=status.HTTP_200_OK)
async def get_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id of {post_id} does not exist.")

    return {"post_detail": post}


@app.delete("/posts/{post_id}", tags=['posts'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    index = find_post_index(post_id)
    
    if index is None:
        raise HTTPException(status_code=404, detail='there is no post with this provided id.')
        
    fake_db.pop(index)
    return {'message': f'post with id of {post_id} has been deleted successfully'}


@app.put("/posts/{post_id}", tags=['posts'])
async def update_post(post_id: int, post: Post):
    index = find_post_index(post_id)

    if index is None:  # "if not index" cannot be true, because if post_id=1, index=0. "if not index" returns true.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id of {post_id} does not exist.")

    post_dict = post.model_dump()
    post_dict['id'] = post_id
    fake_db[index] = post_dict
    return {"data": post_dict}


if __name__ == '__main__':
    uvicorn.run("crud_post:app", host="127.0.0.1", port=8000, reload=True)  
