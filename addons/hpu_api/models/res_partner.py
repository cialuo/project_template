from odoo import models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    def write(self, values):
        name = self.name
        res = super(ResPartner, self).write(values)
        for record in self:
            self._event('on_res_partner_updated').notify(record)
        return res