from odoo import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    is_instructor = fields.Boolean("Instructor", default=False)

    session_ids = fields.Many2many('openacademy.session', 'openacademy_instructor_session_rel', 'instructor_id', 'session_id',
        string="Attended Sessions", readonly=True)