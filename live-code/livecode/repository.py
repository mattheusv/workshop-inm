from http import HTTPStatus
from urllib.parse import urlencode

import requests

from livecode.models import Character


class CharacterRepository:
    def __init__(self, url):
        self.url = url

    def create(self, character):
        character_data = self.validate(character)

        return Character(
            character_data["name"], character_data["gender"], character_data["id"]
        )

    def validate(self, character):
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
