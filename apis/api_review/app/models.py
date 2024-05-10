from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
from .functionalities.api import get_game_info_api
from config.local import config
from werkzeug.security import generate_password_hash, check_password_hash
import sys


db = SQLAlchemy()


def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = config['DATABASE_URI'] if database_path is None else database_path
    db.app = app
    db.init_app(app)
    db.create_all()


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()),
                   server_default=db.text("uuid_generate_v4()"))

    usuario_id = db.Column(db.String(36), nullable=False)

    game_api_id = db.Column(db.String(30), nullable=False)

    title = db.Column(db.String(36), nullable=False)

    comment = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, usuario_id, game_api_id, title, comment):
        self.usuario_id = usuario_id
        self.game_api_id = game_api_id
        self.title = title
        self.comment = comment
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<review %r %r %r>' % (self.usuario_id, self.game_api_id,
                                      self.title)

    def serialize(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'title': self.title,
            'comment': self.comment,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }

    def get_data_with_game(self):
        data = self.serialize()
        game_data = get_game_info_api(self.game_api_id)
        data["game"] = game_data
        return data
