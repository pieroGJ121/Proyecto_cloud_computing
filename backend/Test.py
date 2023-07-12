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
            "user-id" : "1",
            "game_id" : 1942,
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
        pass #manuel

    def test_profile_get_fail(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/profile/failure', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_profile_patch_success(self):
        pass
    def test_profile_delete_success(self):
       pass #manuel
    def test_videogame_data_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/videogame/1942', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_videogame_data_fail(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/videogame/213', headers=self.headers)
        data = json.loads(response.data)
        if response.data == False:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data['success'], False)

    def test_search_data_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/search/platforms',
                                   headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    def test_search_data_fail(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/search/failure', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
    def test_search_querry_success(self):
        pass
    def test_search_querry_fail(self):

        self.incorrect_search_query = {
            "genre": "; invalid because it does not exists",
            "platform": "Todas"
        }
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response = self.client.get('/search/search_query?genre=; invalid because it does not exists&platform=Todas',
                                   headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
    def test_compra_get_success(self):
        pass
    def test_compra_get_id_success(self):
        pass
    def test_compra_post_success(self):
        pass
    def test_oferta_get_success(self):
        pass
    def test_oferta_get_id_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response_game = self.client.get('/videogame/1942', headers=self.headers)
        data_game = json.loads(response_game.data)
        game_id = data_game['game']['api_id']

        response = self.client.get('/oferta/'+ str(game_id) , headers={
            'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_oferta_get_id_fail(self):
        game_id = 1942
        response = self.client.get('/oferta'+ str(game_id) , headers={
            'X-ACCESS-TOKEN': self.user_valid_token})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    def test_oferta_post_success(self):
        self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
        response_game = self.client.get('/videogame/1942', headers=self.headers)
        data_game = json.loads(response_game.data)
        game_id = data_game['game']['api_id']
        self.new_oferta['game_id'] = game_id

        response = self.client.post('/oferta' , headers={
            'X-ACCESS-TOKEN': self.user_valid_token}, json=self.new_oferta)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_oferta_post_fail(self):
        
        response = self.client.post('/oferta' , headers={
            'X-ACCESS-TOKEN': self.user_valid_token}, json=self.new_oferta)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_oferta_patch_success(self):
        pass    #manuel
    def test_oferta_delete_success(self):
        pass    #manuel
    def tearDown(self):
        self.client.delete('/usuarios/' + self.user_id)
