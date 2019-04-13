from marshmallow import validate, Schema, fields
from .util import validate_date_in_future


class FeatureRequestSchema(Schema):
    u"""
    Marshmallow (marshmallow, flask-marshmallow) schema for feature request
    objects with built-in validation for safe insertion into database
    as well as our custom API.
    Loads client and product_area information for their
    respective tables/schemas.
    """
    id = fields.Int(dump_only=True)

    title = fields.Str(
        required=True,
        validate=[validate.Length(min=5, max=255)]
    )
    description = fields.Str(
        required=True,
        validate=[validate.Length(min=5)])

    client_id = fields.Int(
        required=True,
        load_from='client'
    )
    client = fields.Str(dump_only=True)
    client_priority = fields.Int(
        required=True,
        validate=[validate.Range(min=1, max=5)]
    )

    product_area_id = fields.Int(
        required=True,
        load_from='product_area'
    )
    product_area = fields.Str(dump_only=True)

    target_date = fields.Date(
        required=True,
        validate=[validate_date_in_future],
        error_messages={
            'null': {
                'message': 'Date should be in the format YYYY-MM-DD',
                'code': 400
            },
            'validator_failed': {
                'message': 'Date should be in the format YYYY-MM-DD',
                'code': 400
            },
            'required': {
                'message': 'Target date is required (YYYY-MM-DD format)',
                'code': 400
            }
        }
    )
    created_on = fields.Date(dump_only=True)
    updated_on = fields.Date(dump_only=True)


class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)


class ProductAreaSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
