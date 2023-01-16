from pydantic import BaseModel


class Article(BaseModel):
    id: int
    title: str
    actual_content: str
    summary: str
    category: str
    published_date: str
    image_url: str
    url: str
