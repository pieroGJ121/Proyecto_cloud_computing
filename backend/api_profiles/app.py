from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from authentication import authorize
from models import db, Usuario, setup_db
from datetime import datetime
from functionalities.validate_email import validar_correo
import datetime
from config.local import config
import jwt


def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        setup_db(app, test_config["database_path"] if test_config else None)
        CORS(app, support_credentials=True)

    # Todo referente a la pagina de "profile" va aqui
    @app.route("/profile", methods=["GET"])
    # @authorize
    def get_profile():
        current_user_id = request.headers["user-id"]
        current_user = Usuario.query.get(current_user_id)
        return jsonify({"success": True, "user": current_user.serialize()}), 200

    @app.route("/profile", methods=["PATCH"])
    # @authorize
    def change_profile():
        error_lists = []
        returned_code = 200
        try:
            current_user_id = request.headers["user-id"]
            current_user = Usuario.query.get(current_user_id)
            body = request.json
            if "name" in body.keys():
                current_user.firstname = body["name"]
            if "lastname" in body.keys():
                current_user.lastname = body["lastname"]
            if "bio" in body.keys():
                current_user.bio = body["bio"]
            if "password" in body.keys():
                password = body["password"]
                if len(password) < 8 and len(password) != 0:
                    returned_code = 404
                else:
                    current_user.password = password

            db.session.commit()
        except Exception as e:
            print("e: ", e)
            returned_code = 500
        finally:
            db.session.close()

        if returned_code == 404:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "La contraseña debe tener al menos 8 caracteres",
                    }
                ),
                returned_code,
            )
        elif returned_code == 200:
            return (
                jsonify(
                    {"success": True, "message": "Usuario actualizado correctamente"}
                ),
                returned_code,
            )
        else:
            abort(returned_code)

    @app.route("/profile", methods=["DELETE"])
    # @authorize
    def delete_profile():
        current_user_id = request.headers["user-id"]
        current_user = Usuario.query.get(current_user_id)
        # To give the review and ratings, we must make new endpoints in the other apis
        if current_user:
            current_user.delete()
            db.session.commit()
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "El usuario se ha eliminado correctamete.",
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "El usuario no se ha podido eliminar. Intentalo nuevamente",
                    }
                ),
                500,
            )

    @app.route("/create", methods=["POST"])
    def create_user():
        error_lists = []
        returned_code = 201
        try:
            body = request.json
            if "name" not in body:
                error_lists.append("Name is required")
            else:
                name = body.get("name")

            if "lastname" not in body:
                error_lists.append("Lastname is required")
            else:
                lastname = body.get("lastname")

            if "bio" not in body:
                error_lists.append("Bio is required")
            else:
                bio = body.get("bio")

            if "email" not in body:
                error_lists.append("Email is required")
            else:
                email = body.get("email")

            if "password" not in body:
                error_lists.append("Password is required")
            else:
                password = body.get("password")

            if "confirmationPassword" not in body:
                error_lists.append("Confirmation password is required")
            else:
                confirmationPassword = body.get("confirmationPassword")

            user_db = Usuario.query.filter(Usuario.email == email).first()

            if user_db is not None:
                error_lists.append("Este correo ya está registrado 🙄")
            else:
                if not validar_correo(email):
                    error_lists.append("El correo no es válido 😕")
                if len(password) < 8 or len(confirmationPassword) < 8:
                    error_lists.append(
                        "La contraseña debe tener por lo menos 8 caracteres 🙁"
                    )
                if password != confirmationPassword:
                    error_lists.append("Las contraseñas no coinciden 😣")

            if len(error_lists) > 0:
                returned_code = 400
            else:
                user = Usuario(name, lastname, email, bio, password)
                user_created_id = user.insert()
                print("user_created_id: ", user_created_id)
                token = jwt.encode(
                    {
                        "user_created_id": user_created_id,
                        "exp": datetime.datetime.utcnow()
                        + datetime.timedelta(minutes=30),
                    },
                    config["SECRET_KEY"],
                    config["ALGORYTHM"],
                )
                print("token: ", token)

        except Exception as e:
            print("e: ", e)
            returned_code = 500

        if returned_code == 400:
            return jsonify(
                {
                    "success": False,
                    "errors": error_lists,
                    "message": "Error creating a new user",
                }
            )
        elif returned_code != 201:
            abort(returned_code)
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "token": token,
                        "user_id": user_created_id,
                    }
                ),
                returned_code,
            )

    @app.route("/usuarios/<user_id>", methods=["DELETE"])
    def delete_user(user_id):
        returned_code = 200

        try:
            user = Usuario.query.get(user_id)
            if user is None:
                returned_code = 404

            user.delete()
        except Exception as e:
            print("\te: ", e)
            returned_code = 500

        if returned_code != 200:
            abort(returned_code)
        else:
            return jsonify({"success": True})

    @app.route("/login", methods=["POST"])
    def login():
        error_lists = []
        returned_code = 201
        try:
            body = request.json

            if "email" not in body:
                error_lists.append("Se necesita un correo válido")
            else:
                email = body.get("email")

            if "password" not in body:
                error_lists.append("Se necesita una contraseña válida")
            else:
                password = body.get("password")

            usuario_db = Usuario.query.filter(Usuario.email == email).first()

            if usuario_db is not None:
                if usuario_db.verify_password(password):
                    token = jwt.encode(
                        {
                            "usuario_created_id": usuario_db.id,
                            "exp": datetime.datetime.utcnow()
                            + datetime.timedelta(minutes=60),
                        },
                        config["SECRET_KEY"],
                        config["ALGORYTHM"],
                    )
                else:
                    error_lists.append("El correo o la contraseña no son correctos 🙁")

            else:
                error_lists.append("No hay un usuario registrado con ese correo 😣")

            if len(error_lists) > 0:
                returned_code = 400

        except Exception as e:
            print("e: ", e)
            returned_code = 500

        if returned_code == 400:
            return jsonify(
                {
                    "success": False,
                    "errors": error_lists,
                    "message": "Error login a new user",
                }
            )
        elif returned_code != 201:
            abort(returned_code)
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "token": token,
                        "usuario_id": usuario_db.id,
                    }
                ),
                returned_code,
            )

    @app.route("/usuarios/data", methods=["POST"])
    def data_recovery():
        error_lists = []
        returned_code = 201
        try:
            body = request.json

            if "email" not in body:
                error_lists.append("email is required")
            else:
                email = body["email"]

            if "name" not in body:
                error_lists.append("name is required")
            else:
                name = body["name"]

            usuario_db = Usuario.query.filter(Usuario.email == email).first()

            if usuario_db is not None:
                if email != usuario_db.email or name != usuario_db.firstname:
                    returned_code = 400
                    error_lists.append(
                        "Datos de acceso incorrectos. Intente nuevamente &#128577;"
                    )
            else:
                returned_code = 400
                error_lists.append(
                    "No hay ningún usuario registrado con esos datos &#128577;"
                )

            if len(error_lists) > 0:
                returned_code = 400

        except Exception as e:
            print("e: ", e)
            returned_code = 500

        if returned_code == 400:
            return jsonify(
                {
                    "success": False,
                    "errors": error_lists,
                    "message": "Error recovering data of usuario",
                }
            )
        elif returned_code != 201:
            abort(returned_code)
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "El usuario y nombre coinciden",
                    }
                ),
                returned_code,
            )

    @app.route("/usuarios/password", methods=["PATCH"])
    def recover_password():
        returned_code = 200
        error_lists = []

        try:
            body = request.json

            if "password1" not in body:
                error_lists.append("Password is required")
            else:
                password1 = body["password1"]

            if "password2" not in body:
                error_lists.append("Confirmation password  is required")
            else:
                password2 = body["password2"]

            if len(password1) < 8 or len(password2) < 8:
                error_lists.append("La contraseña debe tener al menos 8 caracteres 😴")

            if password1 == password2:
                email = body["email"]
                user = Usuario.query.filter_by(email=email).first()
                user.change_password(password1)
            else:
                error_lists.append("Las contraseñas no coinciden 🙁")

            if len(error_lists) > 0:
                returned_code = 400
        except Exception as e:
            print("\te: ", e)
            returned_code = 500

        if returned_code == 400:
            return jsonify(
                {
                    "success": False,
                    "errors": error_lists,
                    "message": "Error when changing password",
                }
            )
        elif returned_code != 200:
            abort(returned_code)
        else:
            return (
                jsonify({"success": True, "message": "Cambio de contraseña exitoso"}),
                200,
            )

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"success": False, "message": "Acceso no autorizado"}), 401

    @app.errorhandler(403)
    def unauthorizedresource(error):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "You don't have permission to access this resource",
                }
            ),
            403,
        )

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({"success": False, "message": "Resource not found"}), 404

    @app.errorhandler(405)
    def use_not_allowed(error):
        return jsonify({"success": False, "message": "Método no permitido"}), 405

    @app.errorhandler(500)
    def method_not_allowed(error):
        return jsonify({"success": False, "message": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8023, debug=True)
