from datetime import datetime, UTC
from typing import Annotated
from fastapi import Response, Cookie, Header, FastAPI, status
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/items/{item_id}')
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

fake_db = [
    {"name": "Flask", "language": "Python Flask", "type": "microframework Flask", "date": datetime.now(UTC), "published": True},
    {"name": "FastAPI", "language": "Python FastAPI", "type": "web framework FastAPI", "date": datetime.now(UTC), "published": True},
    {"name": "Django", "language": "Python Django", "type": "microframework Django", "date": datetime.now(UTC), "published": True},
    {"name": "Starlette", "language": "Python Starlette", "type": "web framework Starlette", "date": datetime.now(UTC), "published": False}
]


class Post(BaseModel):
    name: str
    language: str
    type: str
    date: datetime = datetime.now(UTC)
    published: bool = True

@app.post('/posts/', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    fake_db.append(post.model_dump())
    return post

@app.get('/posts/')
def read_posts(response: Response, published: bool, limit: int, skip: int = 0, 
    ads_id: Annotated[str | None, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None):
    
    response.set_cookie(key="user", value="belarmino.nicolau@bnms.com.br")
    
    print(f"Cookies: {ads_id}")
    print(f"User-Agent: {user_agent}")
    return [post for post in fake_db[skip : skip+limit] if post['published'] is published]

@app.get('/posts/{framework}')
def read_framework_posts(framework: str):
    return {
        "framework": f" {framework} is a great web framework for Python developers", 
        "post": [
            {"Flask": { "language": "Python Flask", "type": "microframework Flask"}}, 
            {"FastAPI": { "language": "Python FastAPI", "type": "web framework FastAPI"}}, 
            {"Django": { "language": "Python Django", "type": "microframework Django"}}, 
            {"Starlette": { "language": "Python Starlette", "type": "web framework Starlette"}}
        
        ]
    }