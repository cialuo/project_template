from odoo import fields, models, _, api


class Session(models.Model):
    _name = 'openacademy.session'
    _description = "OpenAcademy Sessions"

    name = fields.Char(required=True)
    start_date = fields.Date(string=_("Start date"))
    duration = fields.Float(digits=(6, 2), help=_("Duration in days"))
    seats = fields.Integer(string=_("Number of seats"))
    
    instructor_id = fields.Many2one('res.partner', string=_("Instructor"),
        domain=['|', ('is_instructor', '=', True),
                     ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('openacademy.course',
        ondelete='cascade', string=_("Course"), required=True)
    
    attendee_ids = fields.Many2many('res.partner', 'openacademy_session_attendee_rel', 'session_id', 'attendee_id', string=_("Attendees"))

    
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats