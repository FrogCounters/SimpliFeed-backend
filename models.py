from typing import Union

from pydantic import BaseModel

class Article(BaseModel):
    title: str
    summary: str
    category: str
    published_date: str
    url: str
