from odoo import fields, models, _

class Course(models.Model):
    _name = 'openacademy.course'
    _description = "OpenAcademy Courses"
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', ondelete='set null', string=_('Responsible'), index=True)
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string=_("Sessions"))

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)
    
    
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)', 
         _('The title of the course should not be the description'),
        ),
        ('name_unique',
        'UNIQUE(name)',
        _('The course title must be unique'),
        ),
    ]
