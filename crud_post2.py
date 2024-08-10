from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from datetime import date
import uvicorn
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: date = date.today()

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="Jonibek_2004",
            database='fastapi',
            cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print("Connection to database is successfull.")
        break

    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(3)

@app.get("/posts/", tags=['posts'])
async def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {'all data': posts}


@app.post("/posts/", tags=['posts'], status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute(
        "INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()

    return {'new post': new_post}


@app.get("/posts/{post_id}", tags=['posts'], status_code=status.HTTP_200_OK)
async def get_post(post_id: int):
    cursor.execute("SELECT * FROM posts WHERE id=%s", (str(post_id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with this id does not exist.")

    return {'post': post}


@app.delete("/posts/{post_id}", tags=['posts'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(post_id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no post found with this id")

    # return {'message': "Post successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", tags=['posts'], status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post: Post):
    cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *", (post.title, post.content, post.published, str(post_id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no post found with this id")
    
    return {"updated post": updated_post}



if __name__ == "__main__":
    uvicorn.run("crud_post2:app", host="127.0.0.1", port=8000, reload=True)


