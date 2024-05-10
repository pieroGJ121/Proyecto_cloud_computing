import unittest
from config.qa  import config
from app.models import Review
from app import create_app
import json


class ProyectTests(unittest.TestCase):
    def setUp(self):
        # Probably doesn't work because the database path must be towards the
        # user to make the authorize work
        database_path = config['DATABASE_URI']
        self.app = create_app({'database_path': database_path})
        self.client = self.app.test_client()

        self.new_usuario = {
            "name": "Manuel",
            "lastname": "Gonzalez",
            "bio": "Estudiante de la UTEC",
            "email": "manuel.silva@utec.edu.pe",
            "password": "12345678",
            "confirmationPassword": "12345678",
        }

        self.new_review = {
            "game_id": "1942",
            "title": "It's alright",
            "comment": "I am more elaborate",
        }
        response_user = self.client.post(
            '/create', json=self.new_usuario)
        data_user = json.loads(response_user.data)
        self.user_valid_token = data_user['token']
        self.user_id = data_user['user_id']

    def test_review_get_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/review', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_review_get_id_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.post('/review', headers=self.headers,
                                    json=self.new_review)
        data = json.loads(response.data)
        review_id = data["id"]

        response = self.client.get('/review/' + review_id, headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_review_get_id_fail(self):
        game_id = 1942
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/review'+ str(game_id), headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_review_post_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.post('/review', headers=self.headers,
                                    json=self.new_review)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_review_post_fail(self):
        temp_review = self.new_review
        temp_review["title"] = "llllllllllllllllllllllllllllllllllllllllll"
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.post('/review', headers=self.headers,
                                    json=temp_review)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_review_patch_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.post('/review', headers=self.headers,
                                    json=self.new_review)
        data = json.loads(response.data)
        review_id = data["id"]

        temp_review = self.new_review
        temp_review["title"] = "More interesting"
        response = self.client.patch('/review/' + review_id,
                                     headers=self.headers,
                                     json=temp_review)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_review_patch_fail(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.post('/review', headers=self.headers,
                                    json=self.new_review)
        data = json.loads(response.data)
        review_id = data["id"]

        temp_review = self.new_review
        temp_review["title"] = "llllllllllllllllllllllllllllllllllllllllll"
        response = self.client.patch('/review/' + review_id,
                                     headers=self.headers,
                                     json=temp_review)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_review_delete_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.post('/review', headers=self.headers,
                                    json=self.new_review)
        data = json.loads(response.data)
        print(data)
        review_id = data["id"]

        response = self.client.delete('/review/' + review_id,
                                      headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_review_delete_fail(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.delete('/review/1', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def tearDown(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        self.client.delete('/profile', headers=self.headers)
        temp_headers = self.headers
        temp_headers["user_id"] = self.compra_user_id
        temp_headers['X-ACCESS-TOKEN'] = self.compra_user_valid_token
        self.client.delete('/profile', headers=temp_headers)
