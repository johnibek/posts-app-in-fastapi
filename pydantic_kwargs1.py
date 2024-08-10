from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date


class Post(BaseModel):
    title: str
    description: str
    content: str
    created_at: date

post = Post(
    title="How to learn python in a month",
    description="Some description about this topic",
    content="Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
    created_at=date(2024, 4, 5)
    )

# print(post.model_dump(), type(post.model_dump()))
my_dict = {"id": 1, **post.model_dump()}
my_dict = dict(
    id=1, 
    **post.model_dump()
)
# my_dict.update(post.model_dump())
print(my_dict)
print(post.title)
print(my_dict['title'])
# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8000)