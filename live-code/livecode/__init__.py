from os import getenv

from dotenv import load_dotenv
from flask import Flask
from pymongo import MongoClient

from livecode.api import CharacterApi
from livecode.repository import CharacterRepository


def create_app(dotenv_path=None):
    load_dotenv(dotenv_path)

    app = Flask(__name__)

    mongo_client = MongoClient(getenv("DATABASE_HOST", "mongodb://localhost:27017/"))
    database = mongo_client[getenv("DATABASE", "character")]

    character_repository = CharacterRepository(getenv("RICK_MORTY_API", ""), database)
    character_api = CharacterApi(character_repository)

    @app.route("/characters", methods=("GET",))
    def get_characters():
        return character_api.get()

    @app.route("/characters", methods=("POST",))
    def post_characters():
        return character_api.post()

    return app
