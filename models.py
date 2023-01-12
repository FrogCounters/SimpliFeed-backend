from typing import Union

from pydantic import BaseModel


class Article(BaseModel):
    title: str
    actual_content: str
    summary: str
    category: str
    published_date: str
    url: str
