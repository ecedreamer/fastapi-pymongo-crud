from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from article.db_helpers import article_list, article_create, article_detail, article_update, article_delete
from article.models import ArticleIn, ArticleInDB, ArticleUpdateIn


router = APIRouter(tags=["Article CRUD"])


@router.get("", response_model=List[ArticleInDB])
def article_list_controller(sort: str = None):
    query = {
        "sort": sort
    }
    result = article_list(query)
    return result


@router.post("", response_model=ArticleInDB, status_code=201)
def article_create_controller(article_in: ArticleIn):
    article = article_create(article_in.dict())
    return JSONResponse(article, status_code=201)


@router.get("/{article_id}", response_model=ArticleInDB)
def article_detail_controller(article_id: str):
    article = article_detail(article_id)
    return JSONResponse(article)


@router.put("/{article_id}", response_model=ArticleInDB)
def article_update_controller(article_id: str, data: ArticleUpdateIn):
    article = article_update(article_id, data)
    if article.get("status") == "failure":
        return JSONResponse(article, status_code=400)
    return JSONResponse(article)


@router.delete("/{article_id}", responses={
    200: {
        "description": "Delete request",
        "content": {"application/json": {"example": {"status": "success", "message": "Article deleted successfully."}}},
    },
    400: {
        "description": "Delete request",
        "content": {"application/json": {"example": {"status": "failure", "message": "Article could not be deleted."}}},

    }
})
def article_delete_controller(article_id: str):
    article = article_delete(article_id)
    if article.get("status") == "failure":
        return JSONResponse(article, status_code=400)
    return JSONResponse(article, status_code=200)
