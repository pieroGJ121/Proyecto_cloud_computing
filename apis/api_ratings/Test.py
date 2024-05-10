import unittest
from config.qa  import config
from app.models import Ratings
from app import create_app
import json


class ProyectTests(unittest.TestCase):
    def setUp(self):
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
        self.new_rating = {
            "game_id": "1942",
            "score": 10,
        }

        response_user = self.client.post(
            '/create', json=self.new_usuario)
        data_user = json.loads(response_user.data)
        self.user_valid_token = data_user['token']
        self.user_id = data_user['user_id']

        response_user = self.client.post(
            '/create', json=self.compra_usuario)
        data_user = json.loads(response_user.data)
        self.compra_user_valid_token = data_user['token']
        self.compra_user_id = data_user['user_id']

        self.headers = {
            "content-type": 'application/json',
            "user_id": self.user_id
        }

    def test_rating_get_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/rating', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_rating_get_id_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.post('/rating', headers=self.headers,
                                    json=self.new_rating)
        data = json.loads(response.data)
        rating_id = data["id"]

        response = self.client.get('/rating/' + rating_id, headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_rating_get_id_fail(self):
        game_id = 1942
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/rating'+ str(game_id), headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_rating_post_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.post('/rating', headers=self.headers,
                                    json=self.new_rating)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_rating_post_fail(self):
        temp_rating = self.new_rating
        temp_rating["score"] = "failure"
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.post('/rating', headers=self.headers,
                                    json=temp_rating)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_rating_patch_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.post('/rating', headers=self.headers,
                                    json=self.new_rating)
        data = json.loads(response.data)
        rating_id = data["id"]

        temp_rating = self.new_rating
        temp_rating["score"] = 4
        response = self.client.patch('/rating/' + rating_id,
                                     headers=self.headers,
                                     json=temp_rating)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_rating_patch_fail(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.post('/rating', headers=self.headers,
                                    json=self.new_rating)
        data = json.loads(response.data)
        rating_id = data["id"]

        temp_rating = self.new_rating
        temp_rating["score"] = "failure"
        response = self.client.patch('/rating/' + rating_id,
                                     headers=self.headers,
                                     json=temp_rating)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_rating_delete_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.post('/rating', headers=self.headers,
                                    json=self.new_rating)
        data = json.loads(response.data)
        print(data)
        rating_id = data["id"]

        response = self.client.delete('/rating/' + rating_id,
                                      headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_rating_delete_fail(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.delete('/rating/1', headers=self.headers)
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
