from marshmallow import Schema, fields, validate, EXCLUDE


class AddToolsInputs(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(validate=validate.Length(min=1, max=50), required=True)
    description = fields.Str(validate=validate.Length(min=1, max=150), required=True)