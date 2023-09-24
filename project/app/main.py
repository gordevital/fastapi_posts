from fastapi import FastAPI
from fastapi.security import HTTPBasic

from app.routes import posts, users

from app.db import init_db, get_session

app = FastAPI(docs_url="/api/docs", redoc_url=None, openapi_url="/api/v1/openapi.json")
app.include_router(posts.router, tags=["posts"])
app.include_router(users.router, tags=["users"])

security = HTTPBasic()

@app.on_event("startup")
def on_startup():
    init_db()