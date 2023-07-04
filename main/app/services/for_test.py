from fastapi.testclient import TestClient


class ForTest:

    existing_user_to_sing_up = {
            "login": "user001",
            "name": "user",
            "surname": "001",
            "password": "12345678",
            "confirm_password": "12345678"
        }

    existing_user_for_login = {
        "username": "user001",
        "password": "12345678"
    }

    user_to_sing_up = {
            "login": "user002",
            "name": "user",
            "surname": "002",
            "password": "12345678",
            "confirm_password": "12345678"
        }

    user_for_login = {
        "username": "user002",
        "password": "12345678"
    }

    @classmethod
    def set_access_token(cls, client: TestClient):
        return client.post('/login', data=cls.existing_user_for_login).json()
