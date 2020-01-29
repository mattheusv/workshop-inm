import json
from unittest import TestCase, mock

from livecode import create_app
from tests.factories import CharacterFactory


def _parse_response_data(data):
    return json.loads(data.decode("utf-8").replace("''", '""'))


class CharacterResourceTestCase(TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

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

    def test_post_valid_character_201(self):
        response = self.client.post("/characters")

        self.assertEqual(response.status_code, 201, str(response.data))

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
            response = self.client.post("/characters", data=json_request)
            resp_json = _parse_response_data(response.data)

            json_expect = {
                "id": character_expected.id,
                "name": character_expected.name,
                "gender": character_expected.gender,
            }
            self.assertDictEqual(resp_json, json_expect)
