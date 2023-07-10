from flask import (
    Flask,
    jsonify,
    request,
    abort)
from .usuario_controler import usuarios_bp
from .authentication import authorize
from .functionalities.api import do_request_api, get_game_info_api, get_game_info_api
from flask_cors import CORS
from .models import (
    db,
    Usuario,
    Game,
    Compra,
    Oferta,
    setup_db)
from .functionalities.send_email import enviar_correo
from flask_migrate import Migrate

compra = False


def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        app.config['UPLOAD_FOLDER'] = 'static/employees'
        app.register_blueprint(usuarios_bp)
        setup_db(app, test_config['database_path'] if test_config else None)
        CORS(app, origins=['http://localhost:8080'])

        migrate = Migrate(app, db)

    # Verificar si el usuario esta logeado

    @app.route('/verifier_login', methods=['GET'])
    @authorize
    def verify_login():
        return jsonify({"success": True}), 200

    # Todo referente a la pagina de "profile" va aqui
    @app.route('/profile', methods=['GET'])
    @authorize
    def get_profile():
        current_user_id = request.headers["user-id"]
        current_user = Usuario.query.get(current_user_id)
        return jsonify({"success": True,
                        'user': current_user.serialize()}), 200

    @app.route('/profile', methods=['PATCH'])
    @authorize
    def change_profile():
        body = request.json
        current_user_id = request.headers["user-id"]
        current_user = Usuario.query.get(current_user_id)
        nombre = body['name']
        apellido = body['lastname']
        bio = body['bio']
        password = body['password']

        if len(password) < 8 and len(password) != 0:
            return jsonify({"success": False, "message": "La contraseña debe tener al menos 8 caracteres"}), 200

        if len(password) != 0:
            current_user.password = password

        current_user.firstname = nombre
        current_user.lastname = apellido
        current_user.bio = bio

        db.session.commit()

        return jsonify({'success': True, 'message': 'Usuario actualizado correctamente'}), 200

    @app.route('/profile', methods=['DELETE'])
    @authorize
    def delete_profile():
        current_user_id = request.headers["user-id"]
        current_user = Usuario.query.get(current_user_id)
        if current_user:
            compras_eliminar = Compra.query.filter_by(
                usuario_id=current_user.id).all()
            [db.session.delete(i) for i in compras_eliminar]

            ofertas_eliminar = Oferta.query.filter_by(
                usuario_id=current_user.id).all()
            [db.session.delete(i) for i in ofertas_eliminar]

            db.session.delete(current_user)
            db.session.commit()
            return jsonify({'success': True,
                            'message': 'El usuario se ha eliminado correctamete.'}), 200
        else:
            return jsonify({'success': False,
                            'message': 'El usuario no se ha podido eliminar. Intentalo nuevamente'}), 500

    # Todo referente a la pagina de "videogame" va aqui

    @app.route('/videogame/<identificador>', methods=['GET'])
    @authorize
    def get_videogame(identificador):
        game = 0
        returned_code = 200
        ofertas = []
        try:
            game = get_game_info_api(identificador)
            if not game:
                returned_code = 404
            else:
                game_db = Game.query.filter_by(api_id=identificador).first()
                if game_db:
                    ofertas = game_db.get_ofertas()
        except Exception as e:
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()

        if returned_code != 200:
            abort(returned_code)
        else:
            return jsonify({"success": True, 'game': game,
                            "ofertas": ofertas}), 200

    # Todo referente a la pagina de "search" va aqui

    @app.route('/search/genres', methods=['GET'])
    @authorize
    def get_genres():
        genres = do_request_api("fields name; limit 50;", "genres").json()
        return genres

    @app.route('/search/platforms', methods=['GET'])
    @authorize
    def get_platforms():
        platforms = do_request_api("fields name; limit 200;",
                                   "platforms").json()
        return platforms

    @app.route('/search/search_query', methods=['GET'])
    @authorize
    def do_search():
        selection = request.args.to_dict()
        fields = "fields name, first_release_date, cover.image_id;"
        path = "games"
        body = fields + " limit 500; "
        where = ""

        if selection["genre"] != "Todas":
            where = " where genre = " + selection["genre"]

        if selection["platform"] != "Todas":
            if where == "":
                where = "where platforms = " + selection["platform"] + ";"
            else:
                where += " && platforms.name = " + selection["platform"] + ";"

        body += where
        if selection["name"] != "":
            body = ' search "' + selection["name"] + '";'

        results = do_request_api(body, path + "/count").json()["count"]
        offset = 0
        selected = []
        while (results - offset) // 500 >= 0:
            b = body + " offset " + str(offset) + ";"
            selected.extend(do_request_api(b, path).json())
            offset += 500

        return jsonify({'success': True, 'games': selected}), 200

    # Todo referente a la pagina de "purchases" va aqui
    @app.route('/compra', methods=['GET'])
    @authorize
    def get_purchased_games():
        current_user_id = request.headers["user-id"]
        current_user = Usuario.query.get(current_user_id)
        games_bought = current_user.get_games_bought()
        return jsonify({'success': True, 'games': games_bought}), 200

    @app.route('/compra/<identificador>', methods=['GET'])
    @authorize
    def get_compra(identificador):
        current_user_id = request.headers["user-id"]
        purchase = Compra.query.filter_by(user_id=current_user_id,
                                          game_id=identificador).first()
        return jsonify({'success': True, 'compra': purchase.serialize()})

    @app.route('/compra', methods=['POST'])
    @authorize
    def add_compra():
        body = request.json
        current_user_id = request.headers["user-id"]
        current_user = Usuario.query.filter_by(id=current_user_id).first()

        if "id" not in body:
            return jsonify({'success': False, 'message': 'No se ha enviado el id del juego'}), 400
        else:
            try:
                oferta_id = body["id"]
                new_purchase = Compra(oferta_id, current_user_id)
                db.session.add(new_purchase)
                oferta = Oferta.query.get(oferta_id)
                oferta.realizada = True
                db.session.commit()
                enviar_correo(current_user.email, new_purchase.get_data_with_game()['game']['name'], new_purchase.created_at.strftime(
                    "%d/%m/%Y, %H:%M:%S"), new_purchase.id, new_purchase.get_data_with_game()['game']['cover'], new_purchase.get_data_with_game()['oferta']['price'])
                return jsonify({'success': True, 'compra': new_purchase.serialize(), 'juego': new_purchase.get_data_with_game()}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'success': False, 'message': 'No se ha podido realizar la compra'}), 500

    # Todo referente a comprar y hacer ofertas va aqui

    @app.route('/new_game', methods=['POST'])
    @authorize
    def buy_game():
        global compra
        compra = True
        return jsonify({'success': True, 'message': 'Compra casi lista'})

    @app.route('/oferta', methods=['GET'])
    @authorize
    def obtain_ofertas_from_user():
        current_user_id = request.headers["user-id"]
        current_user = Usuario.query.get(current_user_id)
        ofertas = current_user.get_games_being_sold()
        return jsonify({'success': True,
                        'ofertas_pending': ofertas["pending"],
                        'ofertas_done': ofertas["done"], }), 200

    @app.route('/oferta/<identificador>', methods=['GET'])
    @authorize
    def get_oferta(identificador):
        current_user_id = request.headers["user-id"]
        current_user = Usuario.query.get(current_user_id)
        oferta = Oferta.query.filter_by(id=identificador).first()
        if oferta:
            if oferta.usuario_id == current_user_id:
                return jsonify({'success': True, 'oferta': oferta.serialize(), 'game': oferta.get_data_with_game()}), 200
            else:
                abort(403)
        else:
            abort(404)

    @app.route('/oferta', methods=['POST'])
    @authorize
    def new_oferta():
        returned_code = 200
        list_errors = []
        try:
            current_user_id = request.headers["user-id"]
            body = request.json

            if 'game_id' not in body:
                list_errors.append('game_id is required')
            else:
                game_api_id = body['game_id']
                game = Game.query.filter_by(api_id=game_api_id).first()
                if not game:
                    game = Game(game_api_id)
                    db.session.add(game)
                    db.session.commit()
                game_id = game.id

            if 'price' not in body:
                list_errors.append('price is required')
            else:
                price = body['price']
            if 'platform' not in body:
                list_errors.append('plataforma is required')
            else:
                plataforma = body['platform']

            if len(list_errors) > 0:
                returned_code = 400
            else:
                oferta = Oferta(current_user_id, game_id, price, plataforma)

                db.session.add(oferta)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            returned_code = 500
            print(e)
        finally:
            db.session.close()

        if returned_code == 400:
            return jsonify({'success': False,
                            'message': 'Error creating oferta',
                            'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False,
                            'message': 'Error!'}), returned_code
            # abort(returned_code)
        else:
            return jsonify({'success': True, 'message': 'Oferta Created successfully!'}), returned_code

    @app.route('/oferta/<id>', methods=['PATCH'])
    @authorize
    def update_oferta(id):
        returned_code = 200
        list_errors = []
        try:
            oferta = Oferta.query.get(id)
            if not oferta:
                returned_code = 404
            else:
                body = request.json
                if 'price' in body:
                    price = body['price']
                    oferta.price = price
                if 'platform' in body:
                    plataforma = body['platform']
                    oferta.platform = plataforma
                db.session.commit()

        except:
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()

        if returned_code == 404:
            return jsonify({'success': False,
                            'message': 'There is no oferta'}), returned_code
        elif returned_code == 400:
            return jsonify({'success': False,
                            'message': 'Error updating oferta',
                            'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False,
                            'message': 'Error!'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Oferta updated successfully'}), returned_code

    @app.route('/oferta/<id>', methods=['DELETE'])
    @authorize
    def delete_oferta(id):
        returned_code = 200
        try:
            oferta = Oferta.query.get(id)
            if not oferta:
                returned_code = 404
            else:
                db.session.delete(oferta)
                db.session.commit()

        except:
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()

        if returned_code == 404:
            return jsonify({'success': False,
                            'message': 'There is no oferta'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Oferta deleted successfully'}), returned_code

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'message': 'Acceso no autorizado'
        }), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'Método no permitido'
        }), 405

    return app
