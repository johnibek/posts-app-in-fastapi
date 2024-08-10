from pydantic import BaseModel
from datetime import date

class Post(BaseModel):
    title: str
    description: str
    content: str
    created_at: date

my_dict = {
    "title": "title",
    'description': 'description',
    'content': 'content',
    'created_at': date(2023, 3, 23)
}

post = Post(**my_dict)
print(post)