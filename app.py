from flask import Flask,render_template,jsonify,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

login_val = False
email = ''
password = ''
identificador = ''

@app.route('/', methods=['GET'])
def principal():
    global login_val
    if login_val:
        return 'inicio de sesion correcto'
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    global login_val
    if login_val:
        return redirect(url_for('principal'))
    else:
        return render_template('login.html')

@app.route('/data_login', methods=['POST'])
def data_login():
    global login_val,email,password

    email=request.form['email']
    password=request.form['password']

    if email == 'fabrizzio785@gmail.com' and password == '1234':
        login_val = True
        return jsonify({'success': True, 'message':'Inicio de sesion correcto'}),200
    else:
        return jsonify({'success': False, 'message':'Correo y/o contraseña incorrectos. Intente nuevamente &#128577;'}),400

if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))
