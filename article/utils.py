import requests


def get_user_data(url):
    users = send_get_request(url)
    if users:
        return users.get("data")
    else:
        return None


def send_get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None