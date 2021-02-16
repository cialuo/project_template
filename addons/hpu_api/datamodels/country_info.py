from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class CountryInfo(Datamodel):
    _name = "country.info"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)