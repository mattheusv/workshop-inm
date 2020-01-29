from http import HTTPStatus

from flask_restful import Resource, reqparse

from livecode.schemas import CharacterSchema


class CharacterResource(Resource):
    def __init__(self, character_repository, *args, **kwargs):
        self.repository = character_repository
        self.schema = CharacterSchema()
        super().__init__(*args, **kwargs)

    def get(self):
        characters = self.repository.find()
        return self.schema.dump(characters, many=True)

    def post(self):
        import ipdb

        ipdb.set_trace()
        return {}, HTTPStatus.CREATED
