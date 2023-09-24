from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import username, password

from typing import Annotated

from sqlalchemy import select
from sqlmodel import Session

from app.db import init_db, get_session
from app.models import Post, PostCreate

app = FastAPI(docs_url="/api/docs", redoc_url=None, openapi_url="/api/v1/openapi.json")

security = HTTPBasic()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.get("/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username, "password": credentials.password}

@app.get("/posts", response_model=list[Post])
def get_posts(session: Session = Depends(get_session)):
    result = session.execute(select(Post))
    posts = result.scalars().all()
    return [Post(title=post.title, description=post.description, id=post.id) for post in posts]


@app.post("/posts")
def add_post(post: PostCreate, credentials: Annotated[HTTPBasicCredentials, Depends(security)], session: Session = Depends(get_session)):
    if credentials.password == password and credentials.username == username:
        post = Post(title=post.title, description=post.description)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )