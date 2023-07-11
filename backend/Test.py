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
            "confirm_password" : "12345678", 
        }
        self.new_oferta = {
            "game_id" : "dsadsada",
            "price" : 100,
            "platform" : "ps4"
        }
        self.invalid_form = {
            "game_id" : None,
        }

    def test_create_usuario_success(self):
        pass


    def test_1_create_oferta_success(self):
        response = self.client.post('/oferta', json=self.new_oferta )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_2_create_oferta_fail(self):
        response = self.client.post('/oferta', json=self.invalid_form )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    