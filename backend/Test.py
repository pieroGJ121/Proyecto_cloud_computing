import unittest
from config.qa  import config
from app.models import Game , Usuario , Oferta , Compra
from app import create_app
import json

class ProyectTests(unittest.TestCase):
    def setUp(self):
        database_path = config['DATABASE_URI']
        self.app = create_app({'database_path': database_path})
        self.client = self.app.test_client()


        self.new_usuario = {
            "name" : "Manuel",
            "lastname" : "Gonzalez",
            "bio" : "Estudiante de la UTEC",
            "email" : "manuel.silva@utec.edu.pe",
            "password" : "12345678",
            "confirmationPassword" : "12345678",
        }
        self.new_oferta = {
            "game_id" : "dsadsada",
            "price" : 100,
            "platform" : "ps4"
        }
        self.invalid_form = {
            "game_id" : None,
        }

        response_user = self.client.post(
            '/create', json=self.new_usuario)
        data_user = json.loads(response_user.data)
        self.user_valid_token = data_user['token']
        self.user_id = data_user['user_id']

        self.headers = {
            "content-type": 'application/json'
        }

    # def test_create_usuario_success(self):
    #     pass


    # def test_1_create_oferta_success(self):
    #     response = self.client.post('/oferta', json=self.new_oferta, headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['message'])

    # def test_2_create_oferta_fail(self):
    #     response = self.client.post('/oferta', json=self.invalid_form, headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    def test_1_search_tipo(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/search/genres', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def tearDown(self):
        self.client.delete('/usuarios/' + self.user_id)
