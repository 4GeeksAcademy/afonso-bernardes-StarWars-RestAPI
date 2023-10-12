from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "Users"
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
    __tablename__ = "Characters"
    id = db.Column(db.Integer, primary_key=True)
    external_uid = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=True)
    birth_year = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return '<Character %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.external_uid,
            # do not serialize the password, its a security breach
        }