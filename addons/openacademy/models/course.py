from odoo import fields, models, _

class Course(models.Model):
    _name = 'openacademy.course'
    _description = "OpenAcademy Courses"
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', ondelete='set null', string=_('Responsible'), index=True)
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string=_("Sessions"))
    
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_instructor = fields.Boolean(string=_('Is instructor'))
    sessions = fields.Many2many('openacademy.session', string=_('Session'))