from pydantic import BaseModel
from datetime import datetime


class ArticleIn(BaseModel):
    title: str
    image: str | None = None
    content: str


class ArticleUpdateIn(BaseModel):
    title: str | None = None
    image: str | None = None
    content: str | None = None


class ArticleInDB(ArticleIn):
    id: str
    created_at: datetime = datetime.now()
