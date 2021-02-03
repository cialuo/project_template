from odoo import models, fields


class OpaPolicy(models.Model):
    _name="opa.policy"
    
    name = fields.Char(string="Name", required=True)
    policy = fields.Text(string="Policy")
    description = fields.Text(string="Description")
    