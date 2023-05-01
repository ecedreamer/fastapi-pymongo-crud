import unittest
from unittest import mock
from article.utils import get_user_data, send_get_request


class TestUtil(unittest.TestCase):
    @mock.patch("article.utils.send_get_request")
    def test_get_user_data(self, mock_send_get_request):
        mock_send_get_request.return_value = {"data": [1, 2, 3, 4, 5, 6]}
        user_data = get_user_data("https://reqres.in/api/users?page=2")
        self.assertEqual(len(user_data), 6)
        mock_send_get_request.assert_called_once_with("https://reqres.in/api/users?page=2")

    @mock.patch("article.utils.requests")
    def test_send_get_request(self, mocked_requests):
        mocked_response = mock.MagicMock()
        mocked_response.status_code = 200
        mocked_response.json.return_value = {"data": [1, 2, 3, 4, 5, 6]}

        mocked_requests.get.return_value = mocked_response
        response = send_get_request("https://reqres.in/api/users?page=2")
        self.assertEqual(len(response.get("data")), 6)
        self.assertEqual(response.get("data"), [1, 2, 3, 4, 5, 6])
        mocked_requests.get.assert_called_once()
