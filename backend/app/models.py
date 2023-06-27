from flask_sqlalchemy import SQLAlchemy
import uuid
import requests
import secrets
from datetime import datetime
from .functionalities.api import do_request_api
from config.local import config
from flask_login import LoginManager, UserMixin


db = SQLAlchemy()
login_manager = LoginManager()


def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = config['DATABASE_URI'] if database_path is None else database_path
    db.app = app
    db.init_app(app)
    db.create_all()
    login_manager.init_app(db.app)
    db.app.secret_key = secrets.token_hex(32)


# Class for current user
class User(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.email = user.email
        self.password = user.password
        self.firstname = user.firstname
        self.lastname = user.lastname
        self.bio = user.bio


# Logic to load the user
@login_manager.user_loader
def load_user(id):
    usuario = Usuario.query.filter_by(id=id).first()
    if usuario:
        return User(usuario)
    else:
        return None


# Models
class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, nullable=False)

    ofertas = db.relationship('Oferta', backref='game', lazy=True)
    compras = db.relationship('Compra', backref='game', lazy=True)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, id):
        self.api_id = id
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Game %r>' % (self.id)

    def serialize_basic(self):
        body = "fields *; where id = " + id + ";"
        data = do_request_api(body, "games").json()[0]
        return {
            'id': self.id,
            'api_id': self.api_id,
            'name': data["name"],
            'release_year': data["first_release_year"],
            'genres': data["genres"],
            'platforms': data["platforms"],
            'summary': data["summary"],
            'involved_companies': data["involved_companies"],
            'covers': data["covers"],
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
    password = db.Column(db.String(300), unique=False, nullable=False)
    bio = db.Column(db.Text, nullable=False)

    ofertas = db.relationship('Oferta', backref='usuario', lazy=True)
    compras = db.relationship('Compra', backref='usuario', lazy=True)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, firstname, lastname, email, bio, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.bio = bio
        self.password = password
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Usuario %r %r>' % (self.firstname)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'bio': self.bio,
            'password': self.password,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }

    def get_games_bought(self):
        return [compra.get_game() for compra in
                self.compras]

    def get_games_being_sold(self):
        ofertas_pendientes = []
        ofertas_realizadas = []
        for o in self.ofertas:
            if o.realizada == True:
                ofertas_realizadas.append(o.get_game())
            else:
                ofertas_pendientes.append(o.get_game())
        return [ofertas_pendientes, ofertas_realizadas]


class Compra(db.Model):
    __tablename__ = 'compras'
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()),
                   server_default=db.text("uuid_generate_v4()"))
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'),
                           nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, usuario_id, game_id):
        self.usuario_id = usuario_id
        self.game_id = game_id
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Compra %r %r>' % (self.usuario_id, self.game_id)

    def serialize(self):
        return {
            'id': self.id,
            'usuario': self.usuario.serialize(),
            'game': self.game.serialize(),
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }

    def get_game(self):
        game_data = self.game.serialize()
        game_data["bought_at"] = self.created_at
        return game_data


class Oferta(db.Model):
    __tablename__ = 'ofertas'
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()),
                   server_default=db.text("uuid_generate_v4()"))
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'),
                           nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    plataforma = db.Column(db.String(36), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, usuario_id, game_id, price, plataforma):
        self.usuario_id = usuario_id
        self.game_id = game_id
        self.price = price
        self.plataforma = plataforma
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Oferta %r %r>' % (self.usuario_id, self.game_id)

    def serialize(self):
        return {
            'id': self.id,
            'usuario': self.usuario.serialize(),
            'game': self.game.serialize(),
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }

    def get_game(self):
        game_data = self.game.serialize()
        game_data["bought_at"] = self.created_at
        return game_data
