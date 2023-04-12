from fastapi import FastAPI, Request
from article.controllers import router as article_router
from auth.controllers import router as auth_router

app = FastAPI()


app.include_router(article_router, prefix="/articles")
app.include_router(auth_router, prefix="/auth")


@app.get("/")
async def root():
    return {"status": "ok"}
