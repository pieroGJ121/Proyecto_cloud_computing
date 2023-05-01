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
    compras = db.relationship('Compra', backref='game', lazy=True)
    gamepublishers = db.relationship('Game_publisher', backref='ggame_publisher', lazy=True)
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
    
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(300), unique=True , nullable=False)
    bio = db.Column(db.String(500) , nullable=False )
    image = db.Column(db.String(500), nullable=True)
    compras = db.relationship('Compra', backref='usuario', lazy=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True, server_default=db.text("now()"))

    def __init__(self , firstname, lastname , email , bio ):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email 
        self.bio = bio 
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Usuario %r>' % (self.firstname, self.lastname)

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
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True, server_default=db.text("now()"))

    def __init__(self ,usuario_id , game_id ):
        self.usuario_id
        self.game_id
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Compra %r>' % ()

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
    publisher_name = db.Column(db.String(200), unique=True , nullable=False)
    gamepublishers = db.relationship('Game_publisher', backref='pgame_publisher', lazy=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True, server_default=db.text("now()"))

    def __init__(self, id, publisher_name ):
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
    
# Creates models
with app.app_context():
    db.create_all()


# Start the server
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('another way to run this app')
