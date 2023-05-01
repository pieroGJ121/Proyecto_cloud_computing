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
