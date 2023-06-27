from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for,
    abort)
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user)
from .functionalities.validate_email import validar_correo
from flask_cors import CORS
from .models import (
    db,
    Usuario,
    Game,
    Compra,
    Oferta,
    setup_db,
    User)
from .functionalities.send_email import enviar_correo
from flask_migrate import Migrate
import os

compra = False


def create_app(test_config=None):
    app = Flask(__name__, template_folder='../templates',
                static_folder='../static')
    with app.app_context():
        app.config['UPLOAD_FOLDER'] = 'static/employees'
        setup_db(app, test_config['database_path'] if test_config else None)
        CORS(app, origins='*')
        migrate = Migrate(app, db)

    @app.route('/', methods=['GET'])
    def principal():
        if current_user.is_authenticated:
            return render_template('index.html')
        else:
            return redirect(url_for('login'))

    # Todo referente al login va aqui

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            if current_user.is_authenticated:
                return redirect(url_for('principal'))
            else:
                return render_template('login.html')

        elif request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            # Buscar el usuario en la base de datos
            user = Usuario.query.filter_by(email=email).first()
            if user:
                if user.email == email and user.password == password:
                    login_user(User(user), remember=True)
                    return jsonify({'success': True,
                                    'message': 'Inicio de sesion correcto'}), 200
                else:
                    return jsonify({'success': False,
                                    'message': 'Correo y/o contraseña incorrectos. Intente nuevamente &#128577;'}), 400
            else:
                return jsonify({'success': False,
                                'message': 'Este usuario no está registrado &#128577;'}), 400
        else:
            abort(405)

    @app.route('/logout', methods=['GET'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    # Todo referente al "recuperar contrasenia" va aqui

    @app.route('/data_recovery', methods=['POST'])
    def data_recover():

        email = request.form['email']
        name = request.form['name']

        # Buscar el usuario en la base de datos
        user = Usuario.query.filter_by(email=email).first()
        if user:
            if email == user.email and name == user.firstname:
                return jsonify({'success': True,
                                'message': 'El usuario y nombre coinciden'}), 200
            else:
                return jsonify({'success': False,
                                'message': 'Datos de acceso incorrectos. Intente nuevamente &#128577;'}), 400
        else:
            return jsonify({'success': False,
                            'message': 'No hay ningún usuario registrado con esos datos &#128577;'}), 400

    @app.route('/password_recovery', methods=['GET', 'POST'])
    def recover_password():
        if request.method == 'GET':
            return render_template('recover_password.html')
        elif request.method == 'POST':
            password1 = request.form['password1']
            password2 = request.form['password2']

            if password1 == password2:
                email = request.form['email']
                user = Usuario.query.filter_by(email=email).first()
                user.password = password1
                db.session.commit()
                return jsonify({'success': True,
                                'message': 'Cambio de contraseña correcto'}), 200
            else:
                return jsonify({'success': False,
                                'message': 'Las contraseñas no coinciden &#128577;'}), 400
        else:
            abort(405)

    # Todo referente al "Nuevo usuario" va aqui

    @app.route('/new_user', methods=['GET', 'POST'])
    def new_user():
        if request.method == 'GET':
            return render_template('register.html')
        elif request.method == 'POST':
            name = request.form['name']
            lastname = request.form['lastname']
            bio = request.form['bio']
            email = request.form['email']
            password = request.form['password']

            if validar_correo(email):
                em = Usuario.query.filter_by(email=email).first()
                if em:
                    return jsonify({'success': False,
                                    'message': 'Este correo ya está registrado &#128577;'}), 400
                else:
                    new_user = Usuario(name, lastname, email, bio, password)
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(User(new_user), remember=True)
                    return jsonify({'success': True,
                                    'message': 'El correo ingresado es válido &#128577;'}), 200
            else:
                return jsonify({'success': False,
                                'message': 'El correo ingresado no es válido &#128577;'}), 400
        else:
            abort(405)

    # Todo referente a la pagina de "profile" va aqui

    @app.route('/profile', methods=['GET'])
    @login_required
    def profile():
        return render_template('user.html')

    @app.route('/profile_data', methods=['GET', 'PATCH', 'DELETE'])
    @login_required
    def get_profile():
        user = Usuario.query.filter_by(email=current_user.email).first()
        if request.method == 'GET':
            return jsonify({"success": True, 'user': user.serialize()}), 200
        elif request.method == 'PATCH':
            nombre = request.form['username']
            apellido = request.form['lastname']
            bio = request.form['bio']
            password = request.form['password']

            user = Usuario.query.filter_by(email=current_user.email).first()

            user.firstname = nombre
            user.lastname = apellido
            user.bio = bio
            user.password = password

            current_user.firstname = nombre
            current_user.lastname = apellido
            current_user.bio = bio
            current_user.password = password

            db.session.commit()

            return jsonify({'success': True, 'message': 'Usuario actualizado correctamente'}), 200
        elif request.method == 'DELETE':
            if user:
                # Primero es necesario borrar las compras porque sino da error por la relacion existente
                compras_eliminar = Compra.query.filter_by(
                    usuario_id=user.id).all()
                if compras_eliminar:
                    for i in compras_eliminar:
                        db.session.delete(i)
                # Despues de borrar las compras recien se borra el usuario
                db.session.delete(user)
                db.session.commit()
                logout_user()
                return jsonify({'success': True,
                                'message': 'El usuario se ha eliminado correctamete.'}), 200
            else:
                return jsonify({'success': False,
                                'message': 'El usuario no se ha podido eliminar. Intentalo nuevamente'}), 500
        else:
            abort(405)

    # Todo referente a la pagina de "subir juegos" va aqui

    @app.route('/upload_game', methods=['GET', 'POST'])
    @login_required
    def upload_game():
        if request.method == 'GET':
            return render_template('upload_game.html')
        elif request.method == 'POST':
            pass
        else:
            abort(405)

    # Todo referente a la pagina de "juegos subidos por el usuario" va aqui

    @app.route('/seller', methods=['GET', 'POST', 'PATCH', 'DELETE'])
    @login_required
    def update_game():
        if request.method == 'GET':
            return render_template('user_products.html')
        elif request.method == 'POST':
            pass
        elif request.method == 'PATCH':
            pass
        elif request.method == 'DELETE':
            pass
        else:
            abort(405)

    # Todo referente a la pagina de "recuperar las ofertas de ventas del jugador" va aqui
    @app.route('/info_user_game/<identificador>', methods=['GET'])
    @login_required
    def get_all_info_user_game(identificador):
        if request.method == 'GET':
            pass
        else:
            abort(405)

    # Todo referente a la pagina de "videogame" va aqui

    @app.route('/game_data/<identificador>', methods=['GET'])
    @login_required
    def get_videogame(identificador):
        game = 0
        try:
            game = Game.query.get(identificador)
            if not game:
                returned_code = 404
        except Exception as e:
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()

        if returned_code != 200:
            abort(returned_code)
        else:
            return jsonify({"success": True, 'game': game.serialized()}), 200

    @app.route('/videogame', methods=['GET'])
    def videogame():
        return render_template('game.html')

    # Todo referente a la pagina de "search" va aqui

    @app.route('/genre_data', methods=['GET'])
    @login_required
    def get_genre():
        genres = [g.serialize() for g in genre.query.all()]
        return jsonify({"success": True, 'elementos': genres}), 200

    @app.route('/platform_data', methods=['GET'])
    @login_required
    def get_platform():
        platforms = [p.serialize() for p in platform.query.all()]
        return jsonify({"success": True, 'elementos': platforms}), 200

    @app.route('/publisher_data', methods=['GET'])
    @login_required
    def get_publisher():
        publishers = [p.serialize() for p in Publisher.query.all()]
        return jsonify({"success": True, 'elementos': publishers}), 200

    @app.route('/search_query', methods=['GET'])
    @login_required
    def do_search():
        selection = request.args.to_dict()
        selected = game.query

        if selection["genre"] != "Todas":
            id_genre = genre.query.filter_by(
                genre_name=selection["genre"]).first().id
            selected = selected.filter_by(genre_id=id_genre)

        if selection["name"] != "":
            name = selection["name"]
            selected = selected.filter(game.game_name.ilike(f'%{name}%'))

        if selection["publisher"] != "Todas":
            id_publisher = Publisher.query.filter_by(
                publisher_name=selection["publisher"]).first().id
            selected = selected.filter(
                game.game_publisher.has(publisher_id=id_publisher))

        if selection["platform"] != "Todas":
            id_platform = platform.query.filter_by(
                platform_name=selection["platform"]).first().id
            selected = selected.filter(game.game_publisher.has(
                Game_publisher.game_platform.has(platform_id=id_platform)))

        selected = [game.serialize() for game in selected.all()]

        return jsonify({'success': True, 'games': selected}), 200

    @app.route('/search', methods=['GET'])
    @login_required
    def search():
        return render_template('search.html')

    # Todo referente a la pagina de "purchases" va aqui

    @app.route('/purchases', methods=['GET'])
    @login_required
    def purchases():
        return render_template('purchases.html')

    @app.route('/games_purchased', methods=['GET'])
    @login_required
    def get_purchased_games():
        user = Usuario.query.filter_by(email=current_user.email).first()
        games_bought = user.get_games_bought()
        return jsonify({'success': True, 'games': games_bought,
                        "user": user.serialize()})

    @app.route('/compra_data/<identificador>', methods=['GET'])
    @login_required
    def get_compra(identificador):
        user_id = Usuario.query.filter_by(email=current_user.email).first().id
        purchase = Compra.query.filter_by(usuario_id=user_id,
                                          game_id=identificador).first()
        return jsonify({'success': True, 'compra': purchase.serialize()})

    @app.route('/new_compra/<identificador>', methods=['POST'])
    @login_required
    def add_compra(identificador):
        game_id = game.query.filter_by(id=identificador).first().id

        user_id = Usuario.query.filter_by(email=current_user.email).first().id

        new_purchase = Compra(user_id, game_id)

        db.session.add(new_purchase)
        db.session.commit()

        purchase = Compra.query.filter_by(
            usuario_id=user_id, game_id=game_id).first()

        enviar_correo(current_user.email, purchase.serialize()['game']['game_name'], 'Fecha: {}'.format(
            purchase.created_at), 'ID de compra: {}'.format(purchase.id))

        return jsonify({'success': True, 'compra': purchase.serialize()})

    # Todo referente a comprar videogames va aqui

    @app.route('/game_state/<identificador>', methods=['GET'])
    @login_required
    def is_game_bought(identificador):
        user = Usuario.query.filter_by(email=current_user.email).first()
        state = Compra.query.filter_by(usuario_id=user.id,
                                       game_id=int(identificador)).first()

        if state:
            state = 1
        else:
            state = 0

        return jsonify({"success": True,
                        'is_bought': state}), 200

    @app.route('/new_game', methods=['POST'])
    @login_required
    def buy_game():
        global compra
        compra = True
        return jsonify({'success': True, 'message': 'Compra casi lista'})

    @app.route('/new_oferta', methods=['POST'])
    def new_oferta():
        returned_code = 200
        list_errors = []
        try:
            body = request.form

            if 'usuario_id' not in body:
                list_errors.append('usuario_id is required')
            else:
                usuario_id = body['usuario_id']

            if 'game_id' not in body:
                list_errors.append('game_id is required')
            else:
                game_id = body['game_id']

            if 'price' not in body:
                list_errors.append('price is required')
            else:
                price = body['price']

            if 'plataforma' not in body:
                list_errors.append('plataforma is required')
            else:
                plataforma = body['plataforma']

            if len(list_errors) > 0:
                returned_code = 400
            else:
                oferta = Oferta(usuario_id, game_id, price, plataforma)

                db.session.add(oferta)
                db.session.commit()

        except:
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()

        if returned_code == 400:
            return jsonify({'success': False, 'message': 'Error creating ofert', 'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False, 'message': 'Error!'}), returned_code
            # abort(returned_code)
        else:
            return jsonify({'success': True, 'message': 'Ofert Created successfully!'}), returned_code

    @app.route('/ofertas', methods=['GET'])
    def get_ofertas():
        returned_code = 200
        ofertas_list = []
        try:
            ofertas = Oferta.query.all()
            ofertas_list = [oferta.serialize() for oferta in ofertas]
            if not ofertas_list:
                returned_code = 404

        except Exception as e:
            returned_code = 500

        if returned_code != 200:
            abort(returned_code)

        return jsonify({'success': True, 'ofertas': ofertas_list}), returned_code

    @app.route('/oferta/<id>', methods=['DELETE'])
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

        if returned_code != 200:
            return jsonify({'success': False, 'message': 'Error deleting oferta'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Oferta deleted successfully'}), returned_code

    @app.route('/oferta/<id>', methods=['PATCH'])
    def update_oferta(id):
        returned_code = 200
        list_errors = []
        try:
            body = request.json

            oferta = Oferta.query.get(id)
            if not oferta:
                return jsonify({'success': False, 'message': 'Oferta not found'}), 404

            if 'realizada' in body:
                oferta.realizada = body['realizada']

            db.session.commit()

        except:
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()

        if returned_code == 500:
            # abort(returned_code)
            return jsonify({'success': False, 'message': 'Error updating oferta'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Oferta updated successfully'}), returned_code

    @app.route('/checkout', methods=['GET'])
    @login_required
    def checkout():
        global compra
        if compra:
            return render_template('wait.html')
        else:
            return redirect(url_for('principal'))

    @app.route('/resume', methods=['GET'])
    @login_required
    def resume():
        global compra
        if compra:
            compra = False
            return render_template('resume.html')
        else:
            return redirect(url_for('principal'))

    # Error handlers
    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('error401.html'), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('error404.html'), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template('error405.html'), 405

    return app
