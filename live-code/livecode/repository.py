from http import HTTPStatus
from urllib.parse import urlencode

import requests

from livecode.models import Character


class CharacterRepository:
    def __init__(self, url, database):
        self.url = url
        self.database = database
        self.collection = database.character

    def find(self, filters=None):
        documents = self.collection.find(filters)
        characters = []
        for document in documents:
            characters.append(
                Character(document["name"], document["gender"], document["id"])
            )
        return characters

    def create(self, character):
        character_data = self.parse_character(character)

        character = Character(**character_data)

        character_document = {
            "id": character.id,
            "name": character.name,
            "gender": character.gender,
        }

        self.collection.insert_one(character_document)

        return character

    def parse_character(self, character):
        params = {"name": character.name, "gender": character.gender}
        params = urlencode(params)

        url = f"{self.url}character/?{params}"
        response = requests.get(url)

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise ValueError(
                f"Invalid character: Name={character.name} Gender={character.gender}"
            )

        response_data = response.json()
        results = response_data["results"]
        for data in results:
            if data["name"] == character.name and data["gender"] == character.gender:
                return data
        raise ValueError(
            f"Invalid character: Name={character.name} Gender={character.gender}"
        )
