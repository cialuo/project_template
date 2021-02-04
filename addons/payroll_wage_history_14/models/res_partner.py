from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(index=True, translate=True)