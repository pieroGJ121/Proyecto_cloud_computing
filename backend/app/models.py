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


# Models
class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()),
                   server_default=db.text("uuid_generate_v4()"))
    api_id = db.Column(db.Integer, nullable=False)

    ofertas = db.relationship('Oferta', backref='game', lazy=True)

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
        data = get_game_info_api(self.api_id)
        data["id"] = id
        data['created_at'] = self.created_at,
        data['modified_at'] = self.modified_at,
        return data


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()),
                   server_default=db.text("uuid_generate_v4()"))
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(300), unique=True, nullable=False)
    password_hash = db.Column(db.String(400), nullable=False)
    bio = db.Column(db.Text, nullable=False)

    ofertas = db.relationship('Oferta', backref='usuario', lazy=True)
    compras = db.relationship('Compra', backref='usuario', lazy=True)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, firstname, lastname, email, bio, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.bio = bio
        self.password = password
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Usuario %r %r>' % (self.firstname)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            user_created_id = self.id
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()

        return user_created_id

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'bio': self.bio,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }

    def get_games_bought(self):
        return [compra.get_game() for compra in
                self.compras]

    def get_games_being_sold(self):
        ofertas_pending = []
        ofertas_done = []
        for o in self.ofertas:
            if o.realizada is True:
                ofertas_done.append(o.get_game())
            else:
                ofertas_pending.append(o.get_game())
        return {"pending": ofertas_pending, "done": ofertas_done}


class Compra(db.Model):
    __tablename__ = 'compras'
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()),
                   server_default=db.text("uuid_generate_v4()"))
    user_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'),
                        nullable=False)
    oferta_id = db.Column(db.String(36), db.ForeignKey('ofertas.id'),
                          nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, oferta_id, usuario_id):
        self.oferta_id = oferta_id
        self.usuario_id = usuario_id
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Compra %r %r>' % (self.oferta_id, self.user_id)

    def serialize(self):
        return {
            'id': self.id,
            'oferta': self.oferta.serialize(),
            'usuario': self.usuario.serialize(),
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }

    def get_game(self):
        game_data = self.oferta.game.serialize()
        game_data["date"] = self.created_at
        return game_data


class Oferta(db.Model):
    __tablename__ = 'ofertas'
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()),
                   server_default=db.text("uuid_generate_v4()"))

    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'),
                           nullable=False)
    compra = db.relationship('Compra', backref='oferta', lazy=True)
    game_id = db.Column(db.String(36), db.ForeignKey(
        'games.id'), nullable=False)

    price = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(36), nullable=False)

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
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'price': self.price,
            'platform': self.platform,
        }

    def get_game(self):
        game_data = self.game.serialize()
        game_data["date"] = self.created_at
        return game_data

    def has_compra(self):
        if len(self.compra) == 0:
            return False
        else:
            return True