from marshmallow import Schema, fields, post_load

from livecode.models import Character


class CharacterSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    gender = fields.Str()

    @post_load
    def make_character(self, data, **kwargs):
        return Character(**data)
