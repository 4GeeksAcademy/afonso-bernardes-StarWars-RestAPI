from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class Character(db.Model):
    # Reference: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
    id = db.Column(db.Integer, primary_key=True)
    external_uid = db.Column(db.String(120), nullable=True)
    name = db.Column(db.String(120), nullable=True)
    birth_year = db.Column(db.String(120), nullable=True)
    height = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.external_uid,
            "name": self.name,
            "birth_year": self.birth_year,
            "height": self.height
        }
    
class Planet(db.Model):
    # Reference: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
    id = db.Column(db.Integer, primary_key=True)
    external_uid = db.Column(db.String(120), nullable=True)
    name = db.Column(db.String(120), nullable=True)
    climate = db.Column(db.String(120), nullable=True)
    rotation_period = db.Column(db.String(120), nullable=True)
    orbital_period = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.external_uid,
            "name": self.name,
            "climate": self.climate,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period
        }