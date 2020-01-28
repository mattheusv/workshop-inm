from random import randint

import factory
from faker import Faker

from livecode.models import Character

_faker = Faker()

_GENDERS = ("Male", "Female", "Unknown")


class CharacterFactory(factory.Factory):
    id_character = randint(0, 100)
    name = _faker.name()
    gender = _GENDERS[randint(0, len(_GENDERS) - 1)]

    class Meta:
        model = Character
