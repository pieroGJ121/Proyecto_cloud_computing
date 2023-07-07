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


@usuarios_bp.route('/usuarios', methods=['POST'])
def create_user():
    error_lists = []
    returned_code = 201
    try:
        body = request.get_json()

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
            if user_db.email == email:
                error_lists.append(
                    'An account with this email already exists')
            if validar_correo(email):
                error_lists.append('The email is not valid')
            if len(password) < 8:
                error_lists.append('Password must have at least 8 characters')
            if password != confirmationPassword:
                error_lists.append(
                    'password and confirmationPassword does not match')

        if len(error_lists) > 0:
            returned_code = 400
        else:
            user = Usuario(name, lastname, email, bio, password)
            user_created_id = user.insert()

            token = jwt.encode({
                'user_created_id': user_created_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, config['SECRET_KEY'], config['ALGORYTHM'])

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


@usuarios_bp.route('/usuarios', methods=['GET'])
def login():
    error_lists = []
    returned_code = 201
    try:
        body = request.get_json()

        if 'email' not in body:
            error_lists.append('email is required')
        else:
            email = body.get('email')

        if 'password' not in body:
            error_lists.append('password is required')
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
                    "The password doesn't matches the saved password")

        else:
            error_lists.append(
                'There is no usuario with that email')

        if len(error_lists) > 0:
            returned_code = 400

    except Exception as e:
        print('e: ', e)
        returned_code = 500

    if returned_code == 400:
        return jsonify({
            'success': False,
            'errors': error_lists,
            'message': 'Error creating a new usuario'
        })
    elif returned_code != 201:
        abort(returned_code)
    else:
        return jsonify({
            'success': True,
            'token': token,
            'usuario_id': usuario_db.id,
        }), returned_code


@usuarios_bp.route('/usuarios/data', methods=['GET'])
def data_recovery():
    error_lists = []
    returned_code = 201
    try:
        body = request.get_json()

        if 'email' not in body:
            error_lists.append('email is required')
        else:
            email = body.get('email')

        if 'name' not in body:
            error_lists.append('name is required')
        else:
            name = body.get('name')

        usuario_db = Usuario.query.filter(Usuario.email == email).first()

        if usuario_db is not None:
            if email != usuario_db.email or name != usuario_db.firstname:
                returned_code = 400
                error_lists.append(
                    "Datos de acceso incorrectos. Intente nuevamente &#128577;")
        else:
            returned_code = 400
            error_lists.append(
                "No hay ningún usuario registrado con esos datos &#128577;")

        if len(error_lists) > 0:
            returned_code = 400

    except Exception as e:
        print('e: ', e)
        returned_code = 500

    if returned_code == 400:
        return jsonify({
            'success': False,
            'errors': error_lists,
            'message': 'Error recovering data of usuario'
        })
    elif returned_code != 201:
        abort(returned_code)
    else:
        return jsonify({
            'success': True,
            'message': "El usuario y nombre coinciden",
        }), returned_code
