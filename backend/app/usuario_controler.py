#!/usr/bin/env python3

from flask import (
    Blueprint,
    request,
    jsonify,
    abort
)

import jwt
from .functionalities.validate_email import validar_correo
import datetime

from .models import Usuario
from config.local import config

usuarios_bp = Blueprint('/usuarios', __name__)

@usuarios_bp.route('/create', methods=['POST'])
def create_user():
    error_lists = []
    returned_code = 201
    try:
        body = request.json
        if 'name' not in body:
            error_lists.append('Name is required')
        else:
            name = body.get('name')

        if 'lastname' not in body:
            error_lists.append('Lastname is required')
        else:
            lastname = body.get('lastname')

        if 'bio' not in body:
            error_lists.append('Bio is required')
        else:
            bio = body.get('bio')

        if 'email' not in body:
            error_lists.append('Email is required')
        else:
            email = body.get('email')

        if 'password' not in body:
            error_lists.append('Password is required')
        else:
            password = body.get('password')

        if 'confirmationPassword' not in body:
            error_lists.append('Confirmation password is required')
        else:
            confirmationPassword = body.get('confirmationPassword')

        user_db = Usuario.query.filter(Usuario.email == email).first()

        if user_db is not None:
            error_lists.append(
                    'Este correo ya está registrado 🙄')
        else:
            if not validar_correo(email):
                error_lists.append('El correo no es válido 😕') 
            if len(password) < 8 or len(confirmationPassword) < 8:
                error_lists.append('La contraseña debe tener por lo menos 8 caracteres 🙁')
            if password != confirmationPassword:
                error_lists.append(
                    'Las contraseñas no coinciden 😣')

        if len(error_lists) > 0:
            returned_code = 400
        else:
            user = Usuario(name, lastname, email, bio, password)
            user_created_id = user.insert() 
            print('user_created_id: ', user_created_id)
            token = jwt.encode({
                'user_created_id': user_created_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, config['SECRET_KEY'], config['ALGORYTHM'])
            print('token: ', token)

    except Exception as e:
        print('e: ', e)
        returned_code = 500

    if returned_code == 400:
        return jsonify({
            'success': False,
            'errors': error_lists,
            'message': 'Error creating a new user'
        })
    elif returned_code != 201:
        abort(returned_code)
    else:
        return jsonify({
            'success': True,
            'token': token,
            'user_id': user_created_id,
        }), returned_code


@usuarios_bp.route('/usuarios/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    returned_code = 200

    try:
        user = Usuario.query.get(user_id)
        if user is None:
            returned_code = 404

        user.delete()
    except Exception as e:
        print('\te: ', e)
        returned_code = 500

    if returned_code != 200:
        abort(returned_code)
    else:
        return jsonify({
            'success': True
        })


@usuarios_bp.route('/login', methods=['POST'])
def login():
    error_lists = []
    returned_code = 201
    try:
        body = request.json

        if 'email' not in body:
            error_lists.append('Se necesita un correo válido')
        else:
            email = body.get('email')

        if 'password' not in body:
            error_lists.append('Se necesita una contraseña válida')
        else:
            password = body.get('password')

        usuario_db = Usuario.query.filter(Usuario.email == email).first()

        if usuario_db is not None:
            if usuario_db.verify_password(password):
                token = jwt.encode({
                    'usuario_created_id': usuario_db.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
                }, config['SECRET_KEY'], config['ALGORYTHM'])
            else:
                error_lists.append(
                    "El correo o la contraseña no son correctos 🙁")

        else:
            error_lists.append(
                'No hay un usuario registrado con ese correo 😣')

        if len(error_lists) > 0:
            returned_code = 400

    except Exception as e:
        print('e: ', e)
        returned_code = 500

    if returned_code == 400:
        return jsonify({
            'success': False,
            'errors': error_lists,
            'message': 'Error login a new user'
        })
    elif returned_code != 201:
        abort(returned_code)
    else:
        return jsonify({
            'success': True,
            'token': token,
            'usuario_id': usuario_db.id,
        }), returned_code
