from odoo import models, fields, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enforced_policy_enabled = fields.Boolean(default=False, string=_('Enable enforced policy?'), config_parameter='enforced_policy_enabled')
    enforced_policy_url = fields.Char(string=_('Enforced Policy URL'), config_parameter='enforced_policy_url')



