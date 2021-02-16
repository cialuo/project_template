from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class PartnerInfo(Datamodel):
    _name = "partner.info"
    _inherit = "partner.short.info"

    street = fields.String(required=False, allow_none=True)
    street2 = fields.String(required=False, allow_none=True)
    zip_code = fields.String(required=False, allow_none=True)
    city = fields.String(required=False, allow_none=True)
    phone_sanitized = fields.String(required=False, allow_none=True)
    state = NestedModel("state.info")
    country = NestedModel("country.info")
    is_company = fields.Boolean(required=False, allow_none=False)