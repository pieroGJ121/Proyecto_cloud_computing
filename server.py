from flask import (
    Flask
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/project_dbp'
db = SQLAlchemy(app)


# Models
class genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True, server_default=db.text("now()"))
    games_of_genre = db.relationship('game', backref='genre', lazy=True)

    def __init__(self, id, name):
        self.id = id
        self.genre_name = name
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Genre %r>' % (self.name)

    def serialize(self):
        return {
            'id': self.id,
            'genre_name': self.genre_name,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }

class platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True, server_default=db.text("now()"))

    def __init__(self, id, name):
        self.id = id
        self.platform_name = name
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Platform %r>' % (self.platform_name)

    def serialize(self):
        return {
            'id': self.id,
            'platform_name': self.platform_name,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }


class game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(200), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    synopsis = db.Column(db.String(1000), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    image = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True, server_default=db.text("now()"))

    def __init__(self, id, name, genre_id):
        self.id = id
        self.game_name = name
        self.genre_id = genre_id
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Game %r>' % (self.game_name)

    def serialize(self):
        return {
            'id': self.id,
            'game_name': self.game_name,
            'genre_id': self.genre_id,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }
