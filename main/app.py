import asyncio
from contextlib import asynccontextmanager

import uvloop
from fastapi import FastAPI

from article.controllers import router as article_router
from auth.controllers import router as auth_router
from main.logger import logger

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.warning("Application Started----------------------")
    yield
    logger.warning("Application Terminated----------------------")


app = FastAPI(lifespan=lifespan)
app.include_router(article_router, prefix="/articles")
app.include_router(auth_router, prefix="/auth")


@app.get("/")
async def root():
    return {"status": "ok"}
