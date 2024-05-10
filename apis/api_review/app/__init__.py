from flask import (
    Flask,
    jsonify,
    request,
    abort)
from .authentication import authorize
from flask_cors import CORS
from .models import (
    db,
    Review,
    setup_db)
from datetime import datetime


def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        setup_db(app, test_config['database_path'] if test_config else None)
        # Must change the path. Maybe make it general for everybody
        CORS(app, origins=['http://localhost:8080', 'http://localhost:8081'])
    # Todo referente a review

    @app.route('/review', methods=['GET'])
    @authorize
    def obtain_reviews_from_user():
        current_user_id = request.headers["user-id"]
        reviews = Review.query.filter_by(usuario_id=current_user_id).all()
        reviews_serialized = [i.get_data_with_game() for i in reviews]

        return jsonify({'success': True,
                        'reviews': reviews_serialized}), 200


    @app.route('/review/<id>', methods=['GET'])
    @authorize
    def get_reviews(id):
        current_user_id = request.headers["user-id"]
        review = Review.query.get(id)
        if review:
            if review.usuario_id == current_user_id:
                review_data = review.get_data_with_game()
                return jsonify({'success': True,
                                'review': review_data,
                                'game': review_data["game"]}), 200
            else:
                abort(403)
        else:
            abort(404)

    @app.route('/review', methods=['POST'])
    @authorize
    def new_review():
        returned_code = 201
        list_errors = []
        review_id = ''
        try:
            current_user_id = request.headers["user-id"]
            body = request.json

            if 'game_id' not in body:
                list_errors.append('game_id is required')
            else:
                game_api_id = body['game_id']

            if 'title' not in body:
                list_errors.append('title is required')
            else:
                title = body['title']

            if 'comment' not in body:
                list_errors.append('comment is required')
            else:
                comment = body['comment']

            if len(list_errors) > 0:
                returned_code = 400
            else:
                review = Review(current_user_id, game_api_id, title, comment)

                db.session.add(review)
                db.session.commit()
                review_id = review.id
        except Exception as e:
            db.session.rollback()
            returned_code = 500
            print(e)
        finally:
            db.session.close()

        if returned_code == 400:
            return jsonify({'success': False,
                            'message': 'Error creating review',
                            'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False,
                            'message': 'Error!'}), returned_code
            # abort(returned_code)
        else:
            return jsonify({'success': True,
                            'message': 'Review Created successfully!',
                            "id": review_id}), returned_code

    @app.route('/review/<id>', methods=['PATCH'])
    @authorize
    def update_review(id):
        returned_code = 200
        list_errors = []
        try:
            review = Review.query.get(id)
            if not review:
                returned_code = 404
            else:
                body = request.json
                if 'title' in body:
                    title = body['title']
                    review.title = title

                if 'comment' in body:
                    comment = body['comment']
                    review.comment = comment
                db.session.commit()

        except:
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()

        if returned_code == 404:
            return jsonify({'success': False,
                            'message': 'There is no review'}), returned_code
        elif returned_code == 400:
            return jsonify({'success': False,
                            'message': 'Error updating review',
                            'errors': list_errors}), returned_code
        elif returned_code == 500:
            return jsonify({'success': False,
                            'message': 'Error!'}), returned_code
        else:
            return jsonify({'success': True,
                            'message': 'Review updated successfully'}), returned_code

    @app.route('/review/<id>', methods=['DELETE'])
    @authorize
    def delete_review(id):
        returned_code = 200
        try:
            review = Review.query.get(id)
            if not review:
                returned_code = 404
            else:
                db.session.delete(review)
                db.session.commit()

        except:
            db.session.rollback()
            returned_code = 500
        finally:
            db.session.close()

        if returned_code == 404:
            return jsonify({'success': False,
                            'message': 'There is no review'}), returned_code
        else:
            return jsonify({'success': True, 'message': 'Review deleted successfully'}), returned_code




    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'message': 'Acceso no autorizado'
        }), 401

    @app.errorhandler(403)
    def unauthorizedresource(error):
        return jsonify({
            'success': False,
            'message': "You don't have permission to access this resource"
        }), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'Método no permitido'
        }), 405

    @app.errorhandler(500)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

    return app
