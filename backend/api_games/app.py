from flask import Flask, jsonify, request, abort
from authentication import authorize
from functionalities.api import do_request_api, get_game_info_api
from flask_cors import CORS
from datetime import datetime


def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        CORS(app, support_credentials=True)

    @app.route("/videogame/<identificador>", methods=["GET"])
    # @authorize
    def get_videogame(identificador):
        game = 0
        returned_code = 200
        try:
            game = get_game_info_api(identificador)
        except Exception as e:
            returned_code = 500

        if returned_code != 200:
            abort(returned_code)
        else:
            return jsonify({"success": True, "game": game}), 200

    # Todo referente a la pagina de "search" va aqui

    @app.route("/search/<tipo>", methods=["GET"])
    # @authorize
    def get_data_tipo(tipo):
        if tipo == "genres" or tipo == "platforms":
            data_tipo = do_request_api("fields name; limit 200;", tipo).json()
            return jsonify({"success": True, "data": data_tipo}), 200
        else:
            abort(405)

    @app.route("/search/search_query", methods=["GET"])
    # @authorize
    def do_search():
        returned_code = 200
        try:
            selection = request.args.to_dict()
            fields = (
                "fields name, first_release_date, cover.image_id, involved_companies;"
            )
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
                body += ' search "' + selection["name"] + '";'

            results = do_request_api(body, path + "/count").json()["count"]
            offset = 0
            selected = []
            while (results - offset) // 500 >= 0:
                b = body + " offset " + str(offset) + ";"
                selected.extend(do_request_api(b, path).json())
                offset += 500

            valid = []
            for i in selected:
                if (
                    "first_release_date" in i.keys()
                    and "cover" in i.keys()
                    and "involved_companies" in i.keys()
                ):
                    current = {
                        "release_year": datetime.utcfromtimestamp(
                            i["first_release_date"]
                        ).strftime("%d-%m-%Y"),
                        "name": i["name"],
                        "api_id": i["id"],
                        "cover": "https://images.igdb.com/igdb/image/upload/t_1080p/"
                        + i["cover"]["image_id"]
                        + ".jpg",
                    }
                    valid.append(current)
        except Exception as e:
            returned_code = 500
            print(e)

        if returned_code == 500:
            return (
                jsonify({"success": False, "message": "There is an error"}),
                returned_code,
            )
        else:
            return jsonify({"success": True, "games": valid}), returned_code

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
    app.run(host="0.0.0.0", port=8020, debug=True)
