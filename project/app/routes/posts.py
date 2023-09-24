from fastapi import APIRouter, Depends, HTTPException
from app.security import authorize
from sqlmodel import Session
from app.db import get_session
from app.models import Post, PostCreate

router = APIRouter()

@router.get("/posts", response_model=list[Post])
def get_posts(session: Session = Depends(get_session)):
    posts = session.query(Post).all()
    return [Post(title=post.title, description=post.description, id=post.id) for post in posts]

@router.get("/post/{id}", response_model=Post)
def get_post(id: int, session: Session = Depends(get_session)):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return Post(title=post.title, description=post.description, id=post.id)

@router.post("/posts")
def add_post(post: PostCreate, user=Depends(authorize), session: Session = Depends(get_session)):
    post = Post(title=post.title, description=post.description)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.put("/posts/{id}")
def update_post(post: PostCreate, id: int, session: Session = Depends(get_session), auth = Depends(authorize)):
    post_db = session.get(Post, id)
    if not post_db:
        raise HTTPException(status_code=404, detail="Post not found")
    post_db.title = post.title
    post_db.description = post.description
    session.commit()
    session.refresh(post_db)
    return post_db

@router.delete("/posts/{id}")
def delete_post(id: int, session: Session = Depends(get_session), auth = Depends(authorize)):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return {"ok": "True"}