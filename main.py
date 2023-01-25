from create_db import *
from connect_db import *
from models import *

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# uvicorn main:app --reload
# https://fastapi.tiangolo.com/tutorial/path-params/
origins = ["*"]

create_db_script()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    db.execute("SELECT * FROM articles ORDER BY published_date DESC")
    data = db.fetchall()
    return data


@app.get("/article")
async def get_article(news_id: int = 1):
    db.execute("SELECT * FROM articles WHERE news_id=%s ORDER BY published_date DESC", (news_id,))
    data = db.fetchone()
    return data


@app.post("/article")
async def post_article(article: Article):
    try:
        summary = "{"
        for i in article.summary:
            summary += f'"{i}",'
        summary = summary[:-1]
        summary += "}"
        db.execute("INSERT INTO articles (title, actual_content, summary, category, published_date, image_url, url) VALUES (%s, %s, %s, %s, %s, %s, %s)", (
            article.title, article.actual_content, summary, article.category, article.published_date, article.image_url, article.url))
        return JSONResponse(content={"success": "true"}, status_code=200)
    except:
        return JSONResponse(content={"success": "false"})
