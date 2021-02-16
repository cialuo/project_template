from odoo import models, fields, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    backup_s3_aws_url_endpoint = fields.Char(string=_('AWS URL endpoint'), config_parameter='backup_s3.aws_url_endpoint')
    backup_s3_aws_secret_access_key = fields.Char(string=_('AWS secret access key'), config_parameter='backup_s3.aws_secret_access_key')
    backup_s3_aws_access_key_id = fields.Char(string=_('AWS access key'), config_parameter='backup_s3.aws_access_key_id')

