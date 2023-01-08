from fastapi import Depends, FastAPI, HTTPException, status
from article.controllers import router as article_router

app = FastAPI()


app.include_router(article_router, prefix="/articles")


@app.get("/")
def root():
    return {"status": "ok"}
