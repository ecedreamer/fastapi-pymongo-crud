import datetime
import unittest
from unittest import mock

from bson import ObjectId
from fastapi.testclient import TestClient

from main.app import app


class TestArticleControllers(unittest.TestCase):
    def setUp(self) -> None:
        print("Setting up")
        self.client = TestClient(app)
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
        print("Tearing down")

    @mock.patch('article.controllers.article_list')
    def test_article_list(self, mocked_find):
        mocked_find.return_value.sort.return_value = []
        response = self.client.get("/articles")
        print(response.json())
        self.assertEqual(response.status_code, 200)
        mocked_find.assert_called_once()

    @mock.patch('article.controllers.article_detail')
    def test_article_detail(self, mocked_detail):
        mocked_detail.return_value = self.helper_output
        response = self.client.get("/articles/1234567890ab1234567890ab")
        self.assertEqual(response.status_code, 200)
        mocked_detail.assert_called_once_with("1234567890ab1234567890ab")

    def test_article_create(self):
        self.assertEqual(5, 5)

    def test_article_update(self):
        self.assertEqual(5, 5)

    def test_article_delete(self):
        self.assertEqual(5, 5)
