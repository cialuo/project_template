from datetime import timedelta
from odoo import fields, models, _, api, exceptions


class Session(models.Model):
    _name = 'openacademy.session'
    _description = "OpenAcademy Sessions"

    name = fields.Char(required=True)
    start_date = fields.Date(string=_("Start date"), default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help=_("Duration in days"))
    seats = fields.Integer(string=_("Number of seats"))
    
    instructor_id = fields.Many2one('res.partner', string=_("Instructor"),
        domain=['|', ('is_instructor', '=', True),
                     ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('openacademy.course',
        ondelete='cascade', string=_("Course"), required=True)
    
    attendee_ids = fields.Many2many('res.partner', 'openacademy_session_attendee_rel', 'session_id', 'attendee_id', string=_("Attendees"))
    active = fields.Boolean(default=True)
    end_date = fields.Date(string="End Date", store=True,
        compute='_get_end_date', inverse='_set_end_date')
    
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            r.duration = (r.end_date - r.start_date).days + 1
            
    taken_seats = fields.Float(string=_("Taken seats"), compute='_taken_seats')

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats
                
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _('Incorrect seats value'),
                    'message': _("The number of available seats may not be negative"),
                }
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _("Increase seats or remove excess attendees"),
                },
            }
            
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendee_ids(self):
        if self.instructor_id and self.instructor_id in self.attendee_ids:
            raise exceptions.ValidationError(_("A session's instructor can't be an attendee"))
        
        
    attendees_count = fields.Integer(
        string=_("Attendees count"), compute='_get_attendees_count', store=True)
    
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)
            
    color = fields.Integer()
