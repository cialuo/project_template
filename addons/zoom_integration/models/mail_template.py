from odoo import models, fields, _

class MailTemplate(models.Model):
    _inherit = 'mail.template'
    
    user_signature = fields.Boolean(_('Add Signature'),
                                    help=_("If checked, the user's signature will be appended to the text version "
                                         "of the message"))