from sqlmodel import SQLModel, Field


class PostBase(SQLModel):
    title: str
    description: str


class Post(PostBase, table=True):
    id: int = Field(default=None, primary_key=True)


class PostCreate(PostBase):
    pass