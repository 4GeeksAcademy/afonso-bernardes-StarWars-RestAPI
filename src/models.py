from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    favourite_planets = db.relationship("Planet", secondary="favourite_planets")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class Character(db.Model):
    __tablename__ = 'characters'
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
    __tablename__ = 'planets'
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
    
class FavouritePlanet(db.Model):
    __tablename__ = 'favourite_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    
    # user = db.relationship(User, backref=db.backref("favourite_planets", cascade="all, delete-orphan"))
    # planet = db.relationship(Planet, backref=db.backref("favourite_planets", cascade="all, delete-orphan"))