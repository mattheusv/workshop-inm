import json
from http import HTTPStatus
from unittest import TestCase, mock

from faker import Faker

from livecode import create_app
from tests.factories import CharacterFactory


def _parse_response_data(data):
    return json.loads(data.decode("utf-8").replace("''", '""'))


class CharacterResourceTestCase(TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.faker = Faker()

    def test_get_200(self):
        with mock.patch(
            "livecode.repository.CharacterRepository.find", return_value=[]
        ):
            response = self.client.get("/characters")

            self.assertEqual(response.status_code, 200)

    def test_get_response_data(self):
        with mock.patch(
            "livecode.repository.CharacterRepository.find",
            return_value=CharacterFactory.create_batch(50),
        ):
            response = self.client.get("/characters")
            resp_json = _parse_response_data(response.data)

            self.assertEqual(len(resp_json), 50)

    def test_post_invalid_character(self):
        invalid_character = CharacterFactory.create()
        json_request = {
            "name": invalid_character.name,
            "gender": invalid_character.gender,
        }
        error_message_expected = f"Invalid character: Name={invalid_character.name} Gender={invalid_character.gender}"
        with mock.patch(
            "livecode.repository.CharacterRepository.create",
            side_effect=ValueError(error_message_expected),
        ):
            response = self.client.post("/characters", json=json_request)
            resp_json = _parse_response_data(response.data)

            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertDictEqual({"error": error_message_expected}, resp_json)

    def test_post_invalid_character_request(self):
        json_request = {"invalid_field": self.faker.name()}

        error_message_expected = str({"invalid_field": ["Unknown field."]})
        response = self.client.post("/characters", json=json_request)
        resp_json = _parse_response_data(response.data)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertDictEqual({"error": error_message_expected}, resp_json)

    def test_post_valid_character(self):
        character_expected = CharacterFactory.create()

        json_request = {
            "name": character_expected.name,
            "gender": character_expected.gender,
        }

        with mock.patch(
            "livecode.repository.CharacterRepository.create",
            return_value=character_expected,
        ):
            response = self.client.post("/characters", json=json_request)
            resp_json = _parse_response_data(response.data)

            json_expect = {
                "id": character_expected.id,
                "name": character_expected.name,
                "gender": character_expected.gender,
            }
            self.assertEqual(response.status_code, 201, str(response.data))
            self.assertDictEqual(resp_json, json_expect)
