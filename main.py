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
    return {"message": "Hello World"}


@app.get("/articles")
async def get_articles():
    db.execute("SELECT * FROM articles")
    data = db.fetchall()
    return {"message": data}


@app.post("/articles")
async def post_articles(article: Article):
    try:
        db.execute("INSERT INTO articles VALUES (%s, %s, %s, %s, %s, %s)", (
            article.title, article.actual_content, article.summary, article.category, article.published_date, article.url))
        return JSONResponse(content={"success": "true"}, status_code=200)
    except:
        return JSONResponse(content={"success": "false"})
