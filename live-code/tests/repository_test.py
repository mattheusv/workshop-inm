from http import HTTPStatus
from random import randint
from unittest import TestCase, mock

from faker import Faker
from faker.providers import internet

from livecode.repository import CharacterRepository

from .factories import CharacterFactory


class ResponseMock:
    def __init__(self, status_code, json):
        self.status_code = status_code
        self.json_data = json

    def json(self):
        return self.json_data


class CharacterRepositoryTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.faker.add_provider(internet)

        self.repository = CharacterRepository("http://localhost:444")
        # self.repository = CharacterRepository("https://rickandmortyapi.com/api/")

        self.character = CharacterFactory.create(id_character=0)
        self.response_mock = {
            "results": [
                {
                    "id": randint(1, 100),
                    "name": self.character.name,
                    "gender": self.character.gender,
                },
                {
                    "id": randint(1, 100),
                    "name": self.faker.name(),
                    "gender": "Unknown",
                },
            ]
        }

    def test_create_character(self):
        with mock.patch(
            "requests.get", return_value=ResponseMock(HTTPStatus.OK, self.response_mock)
        ):
            new_character = self.repository.create(self.character)

        self.assertNotEqual(new_character.id, 0, "Id of character should be filled")
        self.assertEqual(new_character.name, self.character.name)
        self.assertEqual(new_character.gender, self.character.gender)

    def test_character_is_valid(self):
        with mock.patch(
            "requests.get", return_value=ResponseMock(HTTPStatus.OK, self.response_mock)
        ):
            try:
                self.repository.validate(self.character)
            except ValueError as e:
                self.fail(f"Character is valid: {e}")

    def test_character_is_not_valid(self):
        character = CharacterFactory.create()

        with self.assertRaises(ValueError):
            self.repository.validate(character)
