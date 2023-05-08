from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functionalities.validate_email import validar_correo

app = Flask(__name__)

login_val = False
email = ''
password = ''
nombre = ''
bio = ''


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
    global login_val, email, password

    email = request.form['email']
    password = request.form['password']

    if email == 'fabrizzio785@gmail.com' and password == '1234':
        login_val = True
        return jsonify({'success': True, 'message': 'Inicio de sesion correcto'}), 200
    else:
        return jsonify({'success': False, 'message': 'Correo y/o contraseña incorrectos. Intente nuevamente &#128577;'}), 400

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
    global login_val, email, password, nombre, bio
    nombre = request.form['name']
    bio = request.form['bio']
    email = request.form['email']
    password = request.form['password']

    if validar_correo(email):
        login_val = True
        return jsonify({'success': True, 'message': 'El correo ingresado si es valido &#128577;'}), 200
    else:
        return jsonify({'success': False, 'message': 'El correo ingresado no es valido &#128577;'}), 400

# Todo referente al "Nuevo usuario" va aqui

if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))
