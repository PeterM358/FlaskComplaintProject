from marshmallow import fields, Schema, validate

from schemas.base import AuthBase


class RegisterSchemaRequest(AuthBase):
    first_name = fields.Str(required=True, validate=validate.Length(min=2, max=20))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=20))
    phone = fields.Str(required=True, validate=validate.Length(min=14, max=14))
    iban = fields.String(min_lenght=22, max_lengh=22, required=True)


class LoginSchemaRequest(AuthBase):
    pass
