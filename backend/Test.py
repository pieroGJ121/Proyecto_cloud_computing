import unittest
from config.qa  import config
from app.models import Game, Usuario, Oferta, Compra
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
        self.compra_usuario = {
            "name": "Test",
            "lastname": "s",
            "bio": "Estudiante de la UTEC",
            "email": "coompratest@utec.edu.pe",
            "password": "qwertyuio",
            "confirmationPassword": "qwertyuio",
        }
        self.new_oferta = {
            "game_id": "1942",
            "price": 100,
            "platform": "ps4"
        }
        self.new_rating = {
            "game_id": "1942",
            "score": 10,
        }
        self.new_review = {
            "game_id": "1942",
            "title": "It's alright",
            "comment": "I am more elaborate",
        }
        self.invalid_form = {
            "game_id": None,
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

    # def test_profile_get_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.get('/profile', headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_profile_get_fail(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.get('/profile/failure', headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)

    # def test_profile_patch_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.patch('/profile',
    #                                  headers=self.headers,
    #                                  json=self.new_usuario)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_profile_patch_fail(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     temp_user = self.new_usuario
    #     temp_user["password"] = "1234"
    #     response = self.client.patch('/profile',
    #                                  headers=self.headers,
    #                                  json=temp_user)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)

    # def test_profile_delete_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.delete('/profile',
    #                                   headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_profile_delete_fail(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.delete('/profile/failure',
    #                                   headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)

    # def test_videogame_data_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.get('/videogame/1942', headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_videogame_data_fail(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.get('/videogame/213', headers=self.headers)
    #     data = json.loads(response.data)
    #     if response.data == False:
    #         self.assertEqual(response.status_code, 404)
    #         self.assertEqual(data['success'], False)

    # def test_search_data_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.get('/search/platforms',
    #                                headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_search_data_fail(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.get('/search/failure', headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 405)
    #     self.assertEqual(data['success'], False)

    # def test_search_querry_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.get('/search/search_query?genre=Todas&platform=Todas&name=zelda',
    #                                headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_search_querry_fail(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.get('/search/search_query?genre=; invalid because it does not exists&platform=Todas',
    #                                headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)

    # def test_compra_get_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.get('/compra', headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_compra_get_id_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.post('/oferta', headers=self.headers,
    #                                 json=self.new_oferta)
    #     data = json.loads(response.data)
    #     oferta_id = data["id"]

    #     new_compra = {"id": oferta_id}

    #     response = self.client.post('/compra', headers=self.headers,
    #                                 json=new_compra)
    #     data = json.loads(response.data)
    #     compra_id = data["compra"]["id"]

    #     response = self.client.get('/compra/' + compra_id, headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_compra_get_id_fail(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.get('/compra/failure', headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)

    # def test_compra_post_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.post('/oferta', headers=self.headers,
    #                                 json=self.new_oferta)
    #     data = json.loads(response.data)
    #     oferta_id = data["id"]

    #     new_compra = {"id": oferta_id}

    #     response = self.client.post('/compra', headers=self.headers,
    #                                 json=new_compra)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(data['success'], True)

    # def test_compra_post_fail(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     new_compra = {}
    #     response = self.client.post('/compra', headers=self.headers,
    #                                 json=new_compra)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(data['success'], False)

    # def test_oferta_get_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.get('/oferta', headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_oferta_get_id_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.post('/oferta', headers=self.headers,
    #                                 json=self.new_oferta)
    #     data = json.loads(response.data)
    #     oferta_id = data["id"]

    #     response = self.client.get('/oferta/' + oferta_id, headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_oferta_get_id_fail(self):
    #     game_id = 1942
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.get('/oferta'+ str(game_id), headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    # def test_oferta_post_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.post('/oferta', headers=self.headers,
    #                                 json=self.new_oferta)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['message'])

    # def test_oferta_post_fail(self):
    #     temp_oferta = self.new_oferta
    #     temp_oferta["price"] = "failure"
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.post('/oferta', headers=self.headers,
    #                                 json=temp_oferta)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    # def test_oferta_patch_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.post('/oferta', headers=self.headers,
    #                                 json=self.new_oferta)
    #     data = json.loads(response.data)
    #     oferta_id = data["id"]

    #     temp_oferta = self.new_oferta
    #     temp_oferta["price"] = 100
    #     response = self.client.patch('/oferta/' + oferta_id, headers=self.headers,
    #                                     json=temp_oferta)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['message'])

    # def test_oferta_patch_fail(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.post('/oferta', headers=self.headers,
    #                                 json=self.new_oferta)
    #     data = json.loads(response.data)
    #     oferta_id = data["id"]

    #     temp_oferta = self.new_oferta
    #     temp_oferta["price"] = "failure"
    #     response = self.client.patch('/oferta/' + oferta_id, headers=self.headers,
    #                                     json=temp_oferta)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    # def test_oferta_delete_success(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.post('/oferta', headers=self.headers,
    #                                 json=self.new_oferta)
    #     data = json.loads(response.data)
    #     oferta_id = data["id"]

    #     response = self.client.delete('/oferta/' + oferta_id, headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['message'])

    # def test_oferta_delete_fail(self):
    #     self.headers['X-ACCESS-TOKEN'] = self.user_valid_token
    #     response = self.client.delete('/oferta/1', headers=self.headers)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

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
