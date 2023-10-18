"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, session
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavouritePlanet
import requests
import json 

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoint - 'GET' Users.
@app.route('/users', methods=['GET'])
def get_user():
    users = User.query.all()
    session['current_user'] = users.serialize()[0]
    return jsonify([user.serialize() for user in users]), 200
    
# Endpoint - 'GET' ALL Characters.
@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    return jsonify([char.serialize() for char in characters]), 200

# Endpoint - 'GET' Single Character.
@app.route('/characters/<string:character_id>', methods=['GET'])
def get_character(character_id):
    char = Character.query.filter_by(external_uid=character_id).first_or_404()
    return jsonify(char.serialize()), 200

# Endpoint - 'GET' ALL Planets.
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

# Endpoint - 'GET' Single Planet.
@app.route('/planets/<string:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.filter_by(external_uid=planet_id).first_or_404()
    return jsonify(planet.serialize()), 200

# Endpoint - 'GET' User Favourites.
@app.route('/users/favourites', methods=['GET'])
def get_user_favourites():
    favourite_planets = FavouritePlanet.query.all()
    return jsonify(favourite_planets)

# Endpoint - 'POST' Planet to Favourites.
@app.route('/favourite/planet/<string:planet_id>', methods=['POST'])
def add_favourite_planet(planet_id):
    current_user = User.query.first()
        
# Endpoint - 'POST' Character to Favouritews.
# Endpoint - 'DELETE' Planet from Favourites.
# Endpoint - 'DELETE' Character from Favourites.