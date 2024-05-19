from flask import Flask, jsonify, request, abort
from authentication import authorize
from sqlalchemy.sql import func
from flask_cors import CORS
from models import db, Rating, setup_db


def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        setup_db(app, test_config["database_path"] if test_config else None)
        # Must change the path. Maybe make it general for everybody
        CORS(app)

    @app.route("/rating", methods=["GET"])
    # @authorize
    def obtain_ratings_from_user():
        current_user_id = request.headers["user-id"]
        ratings = Rating.query.filter_by(usuario_id=current_user_id).all()
        ratings_serialized = [i.get_data_with_game() for i in ratings]

        return jsonify({"success": True, "ratings": ratings_serialized}), 200

    @app.route("/rating/<id>", methods=["GET"])
    # @authorize
    def get_rating(id):
        current_user_id = request.headers["user-id"]
        rating = Rating.query.get(id)
        if rating:
            if rating.usuario_id == current_user_id:
                rating_data = rating.get_data_with_game()
                return (
                    jsonify(
                        {
                            "success": True,
                            "rating": rating_data,
                            "game": rating_data["game"],
                        }
                    ),
                    200,
                )
            else:
                abort(403)
        else:
            abort(404)

    @app.route("/rating/avg/<id>", methods=["GET"])
    # @authorize
    def get_avg_rating(id):

        avg = (
            db.session.query(func.avg(Rating.score).label("average"))
            .filter(Rating.game_api_id == id)
            .all()
        )
        amount = Rating.query.filter_by(game_api_id=id).count()

        avg = 0 if (avg[0][0] is None) else round(avg[0][0], 2)

        return (
            jsonify(
                {
                    "success": True,
                    "avg": avg,
                    "amount": amount,
                }
            ),
            200,
        )

    @app.route("/rating", methods=["POST"])
    # @authorize
    def new_rating():
        returned_code = 201
        list_errors = []
        rating_id = ""
        try:
            current_user_id = request.headers["user-id"]
            body = request.json

            if "game_id" not in body:
                list_errors.append("game_id is required")
            else:
                game_api_id = body["game_id"]

            if "score" not in body:
                list_errors.append("score is required")
            else:
                score = body["score"]

            if len(list_errors) > 0:
                returned_code = 400
            else:
                rating = Rating(current_user_id, game_api_id, score)

                db.session.add(rating)
                db.session.commit()
                rating_id = rating.id
        except Exception as e:
            db.session.rollback()
            returned_code = 500
            print(e)
        finally:
            db.session.close()

        if returned_code == 400:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Error creating rating",
                        "errors": list_errors,
                    }
                ),
                returned_code,
            )
        elif returned_code == 500:
            return jsonify({"success": False, "message": "Error!"}), returned_code
            # abort(returned_code)
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "Rating Created successfully!",
                        "id": rating_id,
                    }
                ),
                returned_code,
            )

    @app.route("/rating/<id>", methods=["PATCH"])
    # @authorize
    def update_rating(id):
        returned_code = 200
        list_errors = []
        try:
            rating = Rating.query.get(id)
            if not rating:
                returned_code = 404
            else:
                body = request.json
                if "score" in body:
                    score = body["score"]
                    rating.score = score
                db.session.commit()

        except:
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()

        if returned_code == 404:
            return (
                jsonify({"success": False, "message": "There is no rating"}),
                returned_code,
            )
        elif returned_code == 400:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Error updating rating",
                        "errors": list_errors,
                    }
                ),
                returned_code,
            )
        elif returned_code == 500:
            return jsonify({"success": False, "message": "Error!"}), returned_code
        else:
            return (
                jsonify({"success": True, "message": "Rating updated successfully"}),
                returned_code,
            )

    @app.route("/rating/<id>", methods=["DELETE"])
    # @authorize
    def delete_rating(id):
        returned_code = 200
        try:
            rating = Rating.query.get(id)
            if not rating:
                returned_code = 404
            else:
                db.session.delete(rating)
                db.session.commit()

        except:
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()

        if returned_code == 404:
            return (
                jsonify({"success": False, "message": "There is no rating"}),
                returned_code,
            )
        else:
            return (
                jsonify({"success": True, "message": "Rating deleted successfully"}),
                returned_code,
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
    def method_not_allowed(error):
        return jsonify({"success": False, "message": "Método no permitido"}), 405

    @app.errorhandler(500)
    def method_not_allowed(error):
        return jsonify({"success": False, "message": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8022, debug=True)
