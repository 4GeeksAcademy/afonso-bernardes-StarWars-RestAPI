"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character
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


@app.route('/import_characters')
def import_characters():
    # Reference: https://stackoverflow.com/questions/61977076/how-to-fetch-data-from-api-using-python
    # Reference: https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html
    res = requests.get('https://www.swapi.tech/api/people/')
    response = json.loads(res.text)
    
    data = response["results"]
    for character_data in data:
        character_res = requests.get(character_data["url"])
        character_json = json.loads(character_res.text)
        result = character_json['result']
        properties = result['properties']
        char = Character(external_uid = result['uid'], name = properties['name'], birth_year= properties['birth_year'])
        db.session.add(char)

    db.session.commit()

    return jsonify({"msg": "All the characters were added"}), 200

@app.route('/user', methods=['GET'])
def handle_user():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def handle_characters():
    characters = Character.query.all()
    # https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
    return jsonify([char.serialize() for char in characters]), 200