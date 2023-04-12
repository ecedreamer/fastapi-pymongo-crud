import datetime
import unittest
from unittest import mock

from bson import ObjectId

from article.db_helpers import article_helper, article_list, article_detail, article_update, article_delete


class ArticleCrudTest(unittest.TestCase):
    def setUp(self) -> None:
        print("setup...")
        self.article_in_db = {
            "_id": ObjectId("1234567890ab1234567890ab"),
            "created_at": datetime.datetime(2023, 4, 12),
            "title": "First title"
        }
        self.helper_output = {
            "id": "1234567890ab1234567890ab",
            "created_at": "2023-04-12 00:00:00",
            "title": "First title"
        }

    def tearDown(self) -> None:
        print("teardown...")

    def test_article_helper(self):
        serializable_article = article_helper(self.article_in_db)
        self.assertEqual(serializable_article, self.helper_output)

    @mock.patch('pymongo.collection.Collection.find')
    def test_article_list(self, mock_find):
        mock_find.return_value.sort.return_value = [self.article_in_db]
        articles = article_list()
        mock_find.assert_called_once()
        mock_find.return_value.sort.assert_called_once()
        print(articles)
        self.assertEqual(articles, [self.helper_output])

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_article_detail(self, mock_find_one):
        mock_find_one.return_value = self.article_in_db
        article = article_detail("1234567890ab1234567890ab")
        mock_find_one.assert_called_once()
        self.assertEqual(article, self.helper_output)

    @mock.patch('pymongo.collection.Collection.update_one')
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_article_update(self, mock_find_one, mock_update_one):
        self.article_in_db["title"] = "Modified title"
        mock_find_one.return_value = self.article_in_db
        mock_update_one.return_value.matched_count = 1
        mock_update_one.return_value.modified_count = 1
        updated_article = article_update("1234567890ab1234567890ab", (("title", "Modified title"),))
        mock_find_one.assert_called_once()
        mock_update_one.assert_called_once()
        self.assertEqual(updated_article, self.article_in_db)

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_article_delete(self, mock_delete_one):
        mock_delete_one.return_value.deleted_count = 1
        delete_status = article_delete("1234567890ab1234567890ab")
        mock_delete_one.assert_called_once()
        self.assertEqual(delete_status, {"status": "success", "message": "Article deleted successfully."})
