from flask import (
    Flask
)
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/project_dbp'
db = SQLAlchemy(app)


# Models
class genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))
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

    games_of_platforms = db.relationship('Game_platform', backref='platform',
                                         lazy=True)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

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
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    synopsis = db.Column(db.String(1000), nullable=True)
    image = db.Column(db.String(500), nullable=True)

    compras = db.relationship('Compra', backref='game', lazy=True)
    game_publisher = db.relationship('Game_publisher',
                                     backref='game', lazy=True, uselist=False)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, id, name, genre_id):
        self.id = id
        self.game_name = name
        self.synopsis = ""
        self.image = ""
        self.genre_id = genre_id
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Game %r>' % (self.game_name)

    def serialize(self):
        return {
            'id': self.id,
            'game_name': self.game_name,
            'synopsis': self.synopsis,
            'image': self.image,
            'genre_id': self.genre_id,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()),
                   server_default=db.text("uuid_generate_v4()"))
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(300), unique=True, nullable=False)
    password = db.Column(db.String(300), unique= False, nullable=False)
    bio = db.Column(db.String(500), nullable=False)
    compras = db.relationship('Compra', backref='usuario', lazy=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, firstname, lastname, email, bio):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.bio = bio
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Usuario %r %r>' % (self.firstname, self.lastname)

    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'bio': self.bio,
            'image': self.image,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }


class Compra(db.Model):
    __tablename__ = 'compras'
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()),
                   server_default=db.text("uuid_generate_v4()"))
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'),
                           nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, usuario_id, game_id):
        self.usuario_id
        self.game_id
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Compra %r %r>' % (self.usuario_id, self.game_id)

    def serialize(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'game_id': self.game_id,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }


class Publisher(db.Model):
    __tablename__ = 'publishers'
    id = db.Column(db.Integer, primary_key=True)
    publisher_name = db.Column(db.String(200), unique=True, nullable=False)

    games_published = db.relationship('Game_publisher',
                                      backref='publisher', lazy=True)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, id, publisher_name):
        self.id = id
        self.publisher_name = publisher_name
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Publisher %r>' % (self.publisher_name)

    def serialize(self):
        return {
            'id': self.id,
            'publisher_name': self.publisher_name,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }


class Game_publisher(db.Model):
    __tablename__ = 'game_publishers'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'),
                             nullable=True)

    game_platform = db.relationship('Game_platform',
                                    backref='game_publisher', lazy=True,
                                    uselist=False)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, id, game_id, publisher_id):
        self.id = id
        self.game_id = game_id
        self.publisher_id = publisher_id
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Game_publisher %r>' % (self.id)

    def serialize(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'publisher_id': self.publisher_id,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }


class Game_platform (db.Model):
    __tablename__ = 'game_platforms'
    id = db.Column(db.Integer, primary_key=True)
    game_publisher_id = db.Column(db.Integer,
                                  db.ForeignKey('game_publishers.id'),
                                  nullable=True)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'),
                            nullable=True)
    realese_year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, id, game_publisher_id, platform_id, realese_year):
        self.id = id
        self.game_publisher_id = game_publisher_id
        self.platform_id = platform_id
        self.realese_year = realese_year
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Game_platform %r>' % (self.id)

    def serialize(self):
        return {
            'id': self.id,
            'game_publisher_id': self.game_publisher_id,
            'platform_id': self.platform_id,
            'realese_year': self.realese_year,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }

# Creates models
# with app.app_context():
#    db.create_all()


# Start the server
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('another way to run this app')
