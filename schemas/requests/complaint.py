from marshmallow import fields

from schemas.base import ComplaintBase


class ComplaintSchemaRequest(ComplaintBase):
    photo = fields.String(required=True)
    extension = fields.String(required=True)

