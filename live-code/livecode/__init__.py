from flask import Flask
from flask_restful import Api
from pymongo import MongoClient

from livecode.api import CharacterResource
from livecode.repository import CharacterRepository


def create_app():
    app = Flask(__name__)
    api = Api(app)

    mongo_client = MongoClient()
    database = mongo_client["database"]

    character_repository = CharacterRepository("http://localhost:444", database)

    api.add_resource(
        CharacterResource,
        "/characters",
        resource_class_kwargs={"character_repository": character_repository},
    )

    return app
