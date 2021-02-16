from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class StateInfo(Datamodel):
    _name = "state.info"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)