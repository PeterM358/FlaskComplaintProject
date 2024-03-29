from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models import ComplaintState
from schemas.base import ComplaintBase


class ComplaintSchemaResponse(ComplaintBase):
    id = fields.Int(required=True)
    created_on = fields.DateTime(required=True)
    status = EnumField(ComplaintState, by_value=True)
    photo_url = fields.String(required=True)
    # TODO make nested schema for complainer id
    # complainer = fields.Nested
