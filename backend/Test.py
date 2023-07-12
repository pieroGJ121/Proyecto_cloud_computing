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

        response_user = self.client.post(
            '/create', json=self.new_usuario)
        data_user = json.loads(response_user.data)
        self.user_valid_token = data_user['token']
        self.user_id = data_user['user_id']

        self.headers = {
            "content-type": 'application/json'
        }


    def test_profile_get_success(self):
        pass    #manuel
    def test_profile_patch_success(self):
        pass
    def test_profile_delete_success(self):
       pass #manuel
    def test_videogame_data_success(self):
        pass #manuel
    def test_videogame_data_fail(self):
        pass  #manuel
    def test_search_data_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/search/platforms', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    def test_search_data_fail(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/search/failure', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 205)
        self.assertEqual(data['success'], False)


    def test_search_data_fail(self):
        pass
    def test_search_querry_success(self):
        pass
    def test_search_querry_fail(self):
        pass
    def test_compra_get_success(self):
        pass  
    def test_compra_get_id_success(self):
        pass
    def test_compra_post_success(self):
        pass
    def test_oferta_get_success(self):
        pass    #manuel
    def test_oferta_get_id_success(self):
        pass    #manuel
    def test_oferta_post_success(self):
        pass    #manuel
    def test_oferta_patch_success(self):
        pass    #manuel
    def test_oferta_delete_success(self):
        pass    #manuel
    def tearDown(self):
        self.client.delete('/usuarios/' + self.user_id)
