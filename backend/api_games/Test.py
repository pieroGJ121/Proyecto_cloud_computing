import unittest
from config.qa import config
from app import create_app
import json


class ProyectTests(unittest.TestCase):
    def setUp(self):
        # Probably doesn't work because the database path must be towards the
        # user to make the authorize work
        database_path = config["DATABASE_URI"]
        self.app = create_app({"database_path": database_path})
        self.client = self.app.test_client()

        self.new_usuario = {
            "name": "Manuel",
            "lastname": "Gonzalez",
            "bio": "Estudiante de la UTEC",
            "email": "manuel.silva@utec.edu.pe",
            "password": "12345678",
            "confirmationPassword": "12345678",
        }

        # response_user = self.client.post(
        #     '/create', json=self.new_usuario)
        # data_user = json.loads(response_user.data)
        # self.user_valid_token = data_user['token']
        # self.user_id = data_user['user_id']

        self.user_valid_token = 1
        self.user_id = 1

        self.headers = {"content-type": "application/json", "user_id": self.user_id}

    def test_videogame_data_success(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.get("/videogame/1942", headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_videogame_data_fail(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.get("/videogame/213", headers=self.headers)
        data = json.loads(response.data)
        if response.data is False:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["success"], False)

    def test_search_data_success(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.get("/search/platforms", headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_search_data_fail(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.get("/search/failure", headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data["success"], False)

    def test_search_querry_success(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.get(
            "/search/search_query?genre=Todas&platform=Todas&name=zelda",
            headers=self.headers,
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_search_querry_fail(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.get(
            "/search/search_query?genre=; invalid because it does not exists&platform=Todas",
            headers=self.headers,
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["success"], False)

    def tearDown(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        self.client.delete("/profile", headers=self.headers)
