from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functionalities.validate_email import validar_correo
from app import Usuario,db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/project_dbp'
db.init_app(app)

login_val = False
email = ''
password = ''
nombre = ''
apellido = ''
bio = ''


@app.route('/', methods=['GET'])
def principal():
    global login_val,nombre

    if login_val:
        return render_template('index.html',nombre=nombre)
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

    email=request.form['email']
    password=request.form['password']

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
            return jsonify({'success': True, 'message':'Inicio de sesion correcto'}),200
        else:
            return jsonify({'success': False, 'message':'Correo y/o contraseña incorrectos. Intente nuevamente &#128577;'}),400
    else:
        return jsonify({'success': False, 'message':'Este usuario no está registrado &#128577;'}),400

# Todo referente al login va aqui

# Todo referente al "recuperar contrasenia" va aqui

@app.route('/recover_password', methods=['GET'])
def recover_password():
    return render_template('recover_password.html')


@app.route('/data_recover', methods=['POST'])
def data_recover():
    global email, password

    email = request.form['email']
    name = request.form['name']

    if email == 'fabrizzio785@gmail.com' and name == 'Fabrizzio':
        return jsonify({'success': True, 'message': 'El usuario y nombre coinciden'}), 200
    else:
        return jsonify({'success': False, 'message': 'Datos de acceso incorrectos. Intente nuevamente &#128577;'}), 400


@app.route('/reset_password', methods=['POST'])
def reset_password():
    global password

    password1 = request.form['password1']
    password2 = request.form['password2']

    if password1 == password2:
        password = password1
        return jsonify({'success': True, 'message': 'Cambio de contraseña correcto'}), 200
    else:
        return jsonify({'success': False, 'message': 'Las contraseñas no coinciden &#128577;'}), 400

# Todo referente al "recuperar contrasenia" va aqui

# Todo referente al "Nuevo usuario" va aqui

@app.route('/new_user', methods=['GET'])
def new_user():
    return render_template('register.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    global login_val, nombre, apellido, email, password, bio
    name = request.form['name']
    lastname = request.form['lastname']
    biog = request.form['bio']
    e_mail = request.form['email']
    password1 = request.form['password']

    if validar_correo(e_mail):
        login_val = True
        nombre = name
        apellido = lastname
        email = e_mail
        password = password1
        bio = biog
        new_user = Usuario(firstname=name ,lastname = lastname ,  email=e_mail, bio=biog , password= password1)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'El correo ingresado es válido &#128577;'}), 200
    else:
        return jsonify({'success': False, 'message': 'El correo ingresado no es válido &#128577;'}), 400

# Todo referente al "Nuevo usuario" va aqui

# Todo referente a la pagina de "usuario" va aqui

@app.route('/user/<nm>', methods=['GET'])
def user_page(nm):
    global login_val, nombre
    if login_val:
        if nm != nombre:
            return 'Error, no puede acceder a un perfil que no esta logueado'
        return render_template('profile.html',nm=nm)
    else:
        return redirect(url_for('login'))

# Todo referente a la pagina de "usuario" va aqui


if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))
