from marshmallow import Schema, fields


class CharacterSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    gender = fields.Str()
