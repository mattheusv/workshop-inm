from http import HTTPStatus
from random import randint
from unittest import TestCase, mock

from faker import Faker
from faker.providers import internet
from pymongo import MongoClient

from livecode.repository import CharacterRepository

from .factories import CharacterFactory

faker = Faker()
faker.add_provider(internet)


class ResponseMock:
    def __init__(self, status_code, json):
        self.status_code = status_code
        self.json_data = json

    def json(self):
        return self.json_data


DOCUMENTS_MOCK = [
    {
        "_id": "...",
        "name": faker.name_female(),
        "gender": "Female",
        "id": randint(100, 500),
    },
    {"_id": "...", "name": faker.name(), "gender": "Unknown", "id": randint(100, 500)},
    {
        "_id": "...",
        "name": faker.name_male(),
        "gender": "Male",
        "id": randint(100, 500),
    },
    {
        "_id": "...",
        "name": faker.name_female(),
        "gender": "Female",
        "id": randint(100, 500),
    },
]


class CharacterRepositoryTestCase(TestCase):
    def setUp(self):
        client = MongoClient()
        self.db = client.test_workshop

        self.repository = CharacterRepository("http://localhost:444", self.db)

        self.character = CharacterFactory.create(id=0)
        self.response_mock = {
            "results": [
                {
                    "id": randint(1, 100),
                    "name": self.character.name,
                    "gender": self.character.gender,
                },
                {"id": randint(1, 100), "name": faker.name(), "gender": "Unknown",},
            ]
        }

    @mock.patch("pymongo.collection.Collection.find", return_value=DOCUMENTS_MOCK)
    def test_find_all(self, mock_db):
        characters = self.repository.find()

        self.assertEqual(len(characters), 4)

    @mock.patch("pymongo.collection.Collection.find", return_value=DOCUMENTS_MOCK[0:1])
    def test_find_filter(self, mock_db):
        filter_name = DOCUMENTS_MOCK[0]["name"]
        characters = self.repository.find({"name": filter_name})

        mock_db.assert_called_once_with({"name": filter_name})
        self.assertEqual(len(characters), 1)

    @mock.patch("pymongo.collection.Collection.insert_one", return_value=None)
    def test_create_character(self, mock_db):
        with mock.patch(
            "requests.get", return_value=ResponseMock(HTTPStatus.OK, self.response_mock)
        ):
            new_character = self.repository.create(self.character)

        self.assertNotEqual(new_character.id, 0, "Id of character should be filled")
        self.assertEqual(new_character.name, self.character.name)
        self.assertEqual(new_character.gender, self.character.gender)

    def test_parse_character_is_valid(self):
        with mock.patch(
            "requests.get", return_value=ResponseMock(HTTPStatus.OK, self.response_mock)
        ):
            try:
                self.repository.parse_character(self.character)
            except ValueError as e:
                self.fail(f"Character is valid: {e}")

    def test_parse_character_not_valid(self):
        character = CharacterFactory.create()

        with mock.patch(
            "requests.get", return_value=ResponseMock(HTTPStatus.OK, {"results": []})
        ):
            with self.assertRaises(ValueError):
                self.repository.parse_character(character)

    def test_parse_character_not_valid_404(self):
        character = CharacterFactory.create()

        with mock.patch(
            "requests.get",
            return_value=ResponseMock(HTTPStatus.NOT_FOUND, self.response_mock),
        ):
            with self.assertRaises(ValueError):
                self.repository.parse_character(character)
