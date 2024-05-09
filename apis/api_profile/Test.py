import unittest
from config.qa  import config
from app.models import Usuario
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

        response_user = self.client.post(
            '/create', json=self.new_usuario)
        data_user = json.loads(response_user.data)
        self.user_valid_token = data_user['token']
        self.user_id = data_user['user_id']

        self.headers = {
            "content-type": 'application/json',
            "user_id": self.user_id
        }

    def test_profile_get_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/profile', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_profile_get_fail(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/profile/failure', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_profile_patch_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.patch('/profile',
                                     headers=self.headers,
                                     json=self.new_usuario)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_profile_patch_fail(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        temp_user = self.new_usuario
        temp_user["password"] = "1234"
        response = self.client.patch('/profile',
                                     headers=self.headers,
                                     json=temp_user)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_profile_delete_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.delete('/profile',
                                      headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_profile_delete_fail(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.delete('/profile/failure',
                                      headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def tearDown(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        self.client.delete('/profile', headers=self.headers)
