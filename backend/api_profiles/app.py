from flask import Flask, jsonify, request, abort
from usuario_controler import usuarios_bp
from authentication import authorize
from flask_cors import CORS
from models import db, Usuario, setup_db
from datetime import datetime


def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        app.register_blueprint(usuarios_bp)
        setup_db(app, test_config["database_path"] if test_config else None)
        CORS(app)

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
            if "lastname" in body.keys():
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
