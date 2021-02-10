from odoo import models, fields, _

class HrEmployee(models.Model):
    _inherit='hr.employee'
    
    mobile = fields.Char(string=_('Mobile'))