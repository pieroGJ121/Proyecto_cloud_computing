from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for
)
from flask_migrate import Migrate
from functionalities.validate_email import validar_correo
from app import (
    app,
    db,
    Usuario,
    genre,
    platform,
    Publisher,
    game,
    Compra,
    Game_publisher,
    Game_platform
)
from functionalities.send_email import enviar_correo

migrate = Migrate(app, db)

login_val = False
email = ''
password = ''
nombre = ''
apellido = ''
bio = ''
compra = False


@app.route('/', methods=['GET'])
def principal():
    global login_val

    if login_val:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

# Todo referente al login va aqui


@app.route('/login', methods=['GET'])
def login():
    global login_val
    if login_val:
        return redirect(url_for('principal'))
    else:
        return render_template('login.html')


@app.route('/data_login', methods=['POST'])
def data_login():
    global login_val, email, password, nombre, apellido, bio

    email = request.form['email']
    password = request.form['password']

    # Buscar el usuario en la base de datos
    user = Usuario.query.filter_by(email=email).first()

    if user:
        if user.email == email and user.password == password:
            login_val = True
            email = user.email
            password = user.password
            nombre = user.firstname
            apellido = user.lastname
            bio = user.bio
            return jsonify({'success': True,
                            'message': 'Inicio de sesion correcto'}), 200
        else:
            return jsonify({'success': False,
                            'message': 'Correo y/o contraseña incorrectos. Intente nuevamente &#128577;'}), 400
    else:
        return jsonify({'success': False,
                        'message': 'Este usuario no está registrado &#128577;'}), 400


@app.route('/logout', methods=['GET'])
def logout():
    global login_val, email, password, nombre, apellido, bio
    if login_val:
        login_val = False
        email = ''
        password = ''
        nombre = ''
        apellido = ''
        bio = ''

    return redirect(url_for('login'))


# Todo referente al login va aqui

# Todo referente al "recuperar contrasenia" va aqui

@app.route('/password_recovery', methods=['GET'])
def recover_password():
    return render_template('recover_password.html')


@app.route('/data_recovery', methods=['POST'])
def data_recover():
    global email, password

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


@app.route('/password_change', methods=['POST'])
def reset_password():
    global password

    password1 = request.form['password1']
    password2 = request.form['password2']

    if password1 == password2:
        user = Usuario.query.filter_by(email=email).first()
        password = password1
        user.password = password
        db.session.commit()
        return jsonify({'success': True,
                        'message': 'Cambio de contraseña correcto'}), 200
    else:
        return jsonify({'success': False,
                        'message': 'Las contraseñas no coinciden &#128577;'}), 400

# Todo referente al "recuperar contrasenia" va aqui

# Todo referente al "Nuevo usuario" va aqui


@app.route('/new_user', methods=['GET'])
def new_user():
    return render_template('register.html')


@app.route('/new_user', methods=['POST'])
def create_user():
    global login_val, nombre, apellido, email, password, bio
    name = request.form['name']
    lastname = request.form['lastname']
    biog = request.form['bio']
    e_mail = request.form['email']
    password1 = request.form['password']

    if validar_correo(e_mail):
        em = Usuario.query.filter_by(email=e_mail).first()
        if em:
            return jsonify({'success': False,
                'message': 'Este correo ya está registrado &#128577;'}), 400
        else:
            login_val = True
            nombre = name
            apellido = lastname
            email = e_mail
            password = password1
            bio = biog
            new_user = Usuario(firstname=name, lastname=lastname,  email=e_mail,
                            bio=biog, password=password1)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'success': True,
                            'message': 'El correo ingresado es válido &#128577;'}), 200
    else:
        return jsonify({'success': False,
                        'message': 'El correo ingresado no es válido &#128577;'}), 400

# Todo referente al "Nuevo usuario" va aqui

# Todo referente a la pagina de "profile" va aqui


@app.route('/profile', methods=['GET'])
def profile():
    if login_val:
        return render_template('user.html')
    else:
        return redirect(url_for('principal'))


@app.route('/profile_data', methods=['GET'])
def get_profile():
    user = Usuario.query.filter_by(email=email).first()
    return jsonify({"success": True, 'user': user.serialize()}), 200

# Todo referente a la pagina de "delete-user" va aqui


@app.route('/user_deletion', methods=['POST'])
def delete_user():
    global nombre, apellido, bio, email, password, login_val
    fila_a_eliminar = Usuario.query.filter_by(email=email).first()
    if fila_a_eliminar:
        compras_eliminar = Compra.query.filter_by(usuario_id = fila_a_eliminar.id).all() #Primero es necesario borrar las compras porque sino da error por la relacion existente
        if compras_eliminar:
            for i in compras_eliminar:
                db.session.delete(i)
        db.session.delete(fila_a_eliminar) #Despues de borrar las compras recien se borra el usuario
        db.session.commit()
        login_val = False
        nombre = ''
        apellido = ''
        bio = ''
        email = ''
        password = ''
        return jsonify({'success': True,
                        'message': 'El usuario se ha eliminado correctamete.'}), 200
    else:
        return jsonify({'success': False,
                        'message': 'El usuario no se ha podido eliminar. Intentalo nuevamente'}), 400

# Todo referente a la pagina de "actualizar_datos" va aqui


@app.route('/data_modification', methods=['POST'])
def update_data():

    global nombre, apellido, bio, email, password

    nombre_r = request.form['username']
    apellido_r = request.form['lastname']
    bio_r = request.form['bio']
    #email_r = request.form['email']
    password_r = request.form['password']

    #user2 = Usuario.query.filter_by(email=email_r).first() #Verificar si el correo al que se quiere cambiar ya existe

    #if user2:
        #if user2.email != email:
            #return redirect(url_for('profile'))

    user = Usuario.query.filter_by(email=email).first()

    nombre = nombre_r
    apellido = apellido_r
    bio = bio_r
    password = password_r
    #email = email_r
 
    user.firstname = nombre
    user.lastname = apellido
    user.bio = bio
    #user.email = email
    user.password = password

    db.session.commit()

    return redirect(url_for('principal'))


# Todo referente a la pagina de "videogame" va aqui


@app.route('/videogame_data/<identificador>', methods=['GET'])
def get_videogame(identificador):
    game_platform = game.query.filter_by(id=identificador).first().game_publisher.game_platform.serialize()
    return jsonify({"success": True, 'game_platform': game_platform}), 200


@app.route('/videogame', methods=['GET'])
def videogame():
    return render_template('game.html')


# Todo referente a la pagina de "search" va aqui


@app.route('/genre_data', methods=['GET'])
def get_genre():
    genres = [g.serialize() for g in genre.query.all()]
    return jsonify({"success": True, 'elementos': genres}), 200


@app.route('/platform_data', methods=['GET'])
def get_platform():
    platforms = [p.serialize() for p in platform.query.all()]
    return jsonify({"success": True, 'elementos': platforms}), 200


@app.route('/publisher_data', methods=['GET'])
def get_publisher():
    publishers = [p.serialize() for p in Publisher.query.all()]
    return jsonify({"success": True, 'elementos': publishers}), 200


@app.route('/search_query', methods=['GET'])
def do_search():
    selection = request.args.to_dict()
    selected = game.query

    if selection["genre"] != "Todas":
        id_genre = genre.query.filter_by(genre_name=selection["genre"]).first().id
        selected = selected.filter_by(genre_id=id_genre)

    if selection["name"] != "":
        name = selection["name"]
        selected = selected.filter(game.game_name.ilike(f'%{name}%'))

    selected.join(game.game_publisher)

    if selection["publisher"] != "Todas":
        id_publisher = Publisher.query.filter_by(publisher_name=selection["publisher"]).first().id
        selected = selected.filter(game.game_publisher.has(publisher_id=id_publisher))

    selected.join(Game_publisher.game_platform)

    if selection["platform"] != "Todas":
        id_platform = platform.query.filter_by(platform_name=selection["platform"]).first().id
        selected = selected.filter(game.game_publisher.has(Game_publisher.game_platform.has(platform_id=id_platform)))

    selected = [game.serialize() for game in selected.all()]

    return jsonify({'success': True, 'games': selected}), 200


@app.route('/search', methods=['GET'])
def search():
    global login_val
    if login_val:
        return render_template('search.html')
    else:
        return redirect(url_for('principal'))


# Todo referente a la pagina de "purchases" va aqui


@app.route('/purchases', methods=['GET'])
def purchases():
    global login_val
    if login_val:
        return render_template('purchases.html')
    else:
        return redirect(url_for('principal'))


@app.route('/games_purchased', methods=['GET'])
def get_purchased_games():
    global email
    user = Usuario.query.filter_by(email=email).first()
    games_bought = user.get_games_bought()
    return jsonify({'success': True, 'games': games_bought,
                    "user": user.serialize()})


@app.route('/compra_data/<identificador>', methods=['GET'])
def get_compra(identificador):
    global email
    user_id = Usuario.query.filter_by(email=email).first().id
    purchase = Compra.query.filter_by(usuario_id=user_id,
                                      game_id=identificador).first()
    return jsonify({'success': True, 'compra': purchase.serialize()})


@app.route('/new_compra/<identificador>', methods=['POST'])
def add_compra(identificador):
    global email
    game_id = game.query.filter_by(id=identificador).first().id
    user_id = Usuario.query.filter_by(email=email).first().id

    new_purchase = Compra(user_id, game_id)

    db.session.add(new_purchase)
    db.session.commit()

    purchase = Compra.query.filter_by(usuario_id=user_id, game_id=game_id).first()

    enviar_correo(email, purchase.serialize()['game']['game_name'],'Fecha: {}'.format(purchase.created_at), 'ID de compra: {}'.format(purchase.id))

    return jsonify({'success': True, 'compra': purchase.serialize()})

# Todo referente a comprar videogames va aqui


@app.route('/game_state/<identificador>', methods=['GET'])
def is_game_bought(identificador):
    global email
    user = Usuario.query.filter_by(email=email).first()
    state = Compra.query.filter_by(usuario_id=user.id,
                                   game_id=int(identificador)).first()

    if state:
        state = 1
    else:
        state = 0

    return jsonify({"success": True,
                    'is_bought': state}), 200


@app.route('/new_game', methods=['POST'])
def buy_game():
    global compra
    compra = True
    return jsonify({'success': True, 'message': 'Compra casi lista'})


@app.route('/checkout', methods=['GET'])
def checkout():
    global compra
    if compra:
        return render_template('wait.html')
    else:
        return redirect(url_for('principal'))


@app.route('/resume', methods=['GET'])
def resume():
    global compra
    if compra:
        compra = False
        return render_template('resume.html')
    else:
        return redirect(url_for('principal'))


if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))
