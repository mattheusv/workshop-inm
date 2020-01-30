from http import HTTPStatus

from flask import jsonify, request
from marshmallow.exceptions import ValidationError

from livecode.schemas import CharacterSchema


class CharacterApi:
    def __init__(self, character_repository, *args, **kwargs):
        self.repository = character_repository
        self.schema = CharacterSchema()
        super().__init__(*args, **kwargs)

    def get(self):
        characters = self.repository.find()
        return jsonify(self.schema.dump(characters, many=True))

    def post(self):
        try:
            character = self.schema.load(request.get_json())
            character = self.repository.create(character)
            return jsonify(self.schema.dump(character)), HTTPStatus.CREATED
        except ValueError as e:
            return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
        except ValidationError as e:
            return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
