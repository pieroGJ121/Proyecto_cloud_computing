from flask_sqlalchemy import SQLAlchemy
import uuid
import secrets
from datetime import datetime
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
class genre(db.Model):
    __tablename__ = 'genres'
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
            'name': self.genre_name,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }


class platform(db.Model):
    __tablename__ = 'platforms'
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
            'name': self.platform_name,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }


class game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(200), unique=True, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey(
        'genres.id'), nullable=False)
    synopsis = db.Column(db.String(1000), nullable=True)
    image = db.Column(db.String(500), nullable=True)

    ofertas = db.relationship('Oferta', backref='game', lazy=True)
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
        # DEFAULT IMAGE BY THE MOMENT...
        self.image = "/static/game_images/generic/generic_image.jpeg"
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
            'genre': self.genre.serialize(),
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

    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, usuario_id, game_id):
        self.usuario_id = usuario_id
        self.game_id = game_id
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
            'name': self.publisher_name,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }


class Game_publisher(db.Model):
    __tablename__ = 'game_publishers'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=True)
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
            'game': self.game.serialize(),
            'publisher': self.publisher.serialize(),
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }


class Game_platform (db.Model):
    __tablename__ = 'game_platforms'
    id = db.Column(db.Integer, primary_key=True)
    game_publisher_id = db.Column(db.Integer,
                                  db.ForeignKey('game_publishers.id'),
                                  nullable=True)
    platform_id = db.Column(db.Integer, db.ForeignKey('platforms.id'),
                            nullable=True)
    release_year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True,
                            server_default=db.text("now()"))

    def __init__(self, id, game_publisher_id, platform_id, release_year):
        self.id = id
        self.game_publisher_id = game_publisher_id
        self.platform_id = platform_id
        self.release_year = release_year
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Game_platform %r>' % (self.id)

    def serialize(self):
        return {
            'id': self.id,
            'game_publisher': self.game_publisher.serialize(),
            'platform': self.platform.serialize(),
            'release_year': self.release_year,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }
