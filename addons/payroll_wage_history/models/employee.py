from odoo import models, fields, api
from .. import constants as c
class HrEmployee(models.Model):
  _inherit = c.employee_model
  
  wage_history_rec_count = fields.Integer(
    string = 'Wage History Record(s)',
    compute = '_count_wage_history_rec',
    default = 0,
    store = True,
  )
  
  wage_ids = fields.One2many(c.pwh_model, c.employee_field)
  
  @api.depends('wage_ids')
  def _count_wage_history_rec(self):
    wage_history_env = self.env[c.pwh_model]
    for employee in self:
      rec_count = wage_history_env.search(
        [(c.employee_field, '=', employee.id)], 
        count = True
      )
      employee.wage_history_rec_count = rec_count
    return