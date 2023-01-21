from main.db_config import collections
from datetime import datetime
from bson.objectid import ObjectId


ArticleCollection = collections.get("articles")


def article_helper(article):
    article["id"] = str(article.get("_id"))
    article["created_at"] = str(article.get("created_at"))
    article.pop("_id")
    return article


def article_list(query=None):
    articles = ArticleCollection.find().sort(query.get("sort") if query.get("sort") else "created_at")
    articles_in_db = [article_helper(article) for article in articles]
    return articles_in_db


def article_create(article_in):
    article_in["created_at"] = datetime.now()
    article_id = ArticleCollection.insert_one(article_in).inserted_id
    article = ArticleCollection.find_one({"_id": article_id})
    return article_helper(article)


def article_detail(object_id):
    article = ArticleCollection.find_one({"_id": ObjectId(object_id)})
    return article_helper(article)


def article_update(object_id, data):
    try:
        changed_key_value = {key: value for key, value in data if value is not None}
        update_status = ArticleCollection.update_one({"_id": ObjectId(object_id)}, {"$set": changed_key_value})
        if update_status.matched_count <= 0:
            return {"status": "failure", "message": "Article could not be found."}
        if update_status.modified_count > 0:
            article = ArticleCollection.find_one({"_id": ObjectId(object_id)})
            return article_helper(article)
        else:
            return {"status": "failure", "message": "No modification in the data."}
    except Exception as e:
        return {"status": "failure", "message": f"{e}"}


def article_delete(object_id):
    try:
        delete_status = ArticleCollection.delete_one({"_id": ObjectId(object_id)})
        if delete_status.deleted_count > 0:
            return {"status": "success", "message": f"Article deleted successfully."}
        else:
            return {"status": "failure", "message": "Article could not be deleted."}
    except Exception as e:
        return {"status": "failure", "message": f"{e}"}
