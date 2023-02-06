from typing import Optional

from pydantic import BaseModel, HttpUrl


class ArticleSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    font_url: HttpUrl
    user_id: Optional[int]

    class Config:
        orm_mode = True