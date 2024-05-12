import unittest
from config.qa import config
from models import Review
from app import create_app
import json


class ProyectTests(unittest.TestCase):
    def setUp(self):
        # Probably doesn't work because the database path must be towards the
        # user to make the authorize work
        database_path = config["DATABASE_URI"]
        self.app = create_app({"database_path": database_path})
        self.client = self.app.test_client()

        self.new_review = {
            "game_id": "1942",
            "title": "It's alright",
            "comment": "I am more elaborate",
        }

        self.user_valid_token = 1
        self.user_id = "93cd770c-ef90-4f68-9684-5d8670f48129"

        self.headers = {"content-type": "application/json", "user_id": self.user_id}

    def test_review_get_success(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.get("/review", headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_review_get_id_success(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.post(
            "/review", headers=self.headers, json=self.new_review
        )
        data = json.loads(response.data)
        review_id = data["id"]

        response = self.client.get("/review/" + review_id, headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_review_get_id_fail(self):
        game_id = 1942
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.get("/review" + str(game_id), headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_review_post_success(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.post(
            "/review", headers=self.headers, json=self.new_review
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["message"])

    def test_review_post_fail(self):
        temp_review = self.new_review
        temp_review["title"] = "llllllllllllllllllllllllllllllllllllllllll"
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.post("/review", headers=self.headers, json=temp_review)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_review_patch_success(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.post(
            "/review", headers=self.headers, json=self.new_review
        )
        data = json.loads(response.data)
        review_id = data["id"]

        temp_review = self.new_review
        temp_review["title"] = "More interesting"
        response = self.client.patch(
            "/review/" + review_id, headers=self.headers, json=temp_review
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["message"])

    def test_review_patch_fail(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.post(
            "/review", headers=self.headers, json=self.new_review
        )
        data = json.loads(response.data)
        review_id = data["id"]

        temp_review = self.new_review
        temp_review["title"] = "llllllllllllllllllllllllllllllllllllllllll"
        response = self.client.patch(
            "/review/" + review_id, headers=self.headers, json=temp_review
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_review_delete_success(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.post(
            "/review", headers=self.headers, json=self.new_review
        )
        data = json.loads(response.data)
        print(data)
        review_id = data["id"]

        response = self.client.delete("/review/" + review_id, headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["message"])

    def test_review_delete_fail(self):
        self.headers["X-ACCESS-TOKEN"] = self.user_valid_token
        response = self.client.delete("/review/1", headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def tearDown(self):
        return
