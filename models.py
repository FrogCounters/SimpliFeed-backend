from pydantic import BaseModel


class Article(BaseModel):
    title: str
    actual_content: str
    summary: list
    category: str
    published_date: str
    image_url: str
    url: str
