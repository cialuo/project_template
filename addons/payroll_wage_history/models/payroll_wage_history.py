from odoo import models, fields, api, _
from odoo.exceptions import UserError
from .. import constants as c, utils
class PayrollWageHistory(models.Model):
  _name = c.pwh_model
  _description = 'Payroll Wage History'
  _rec_name = c.revision_field
  
  revision = fields.Char(
    string = 'Revision No.',
    store = True,
    readonly = True,
    index = True,
    compute = '_compute_revision_no_effective_month_year',
  )
  _sql_constraints = [
    (c.revision_field, 'unique ({revision_field})'.format(revision_field=c.revision_field), 'There is only one revision !')
  ]

  effective_date = fields.Date(
    string = 'Effective date',
    default = lambda self: fields.Date.today(),
    readonly = True,
  )
  effective_month = fields.Integer(
    string = 'Effective month',
    store = True,
    readonly = True,
    index = True,
    compute = '_compute_revision_no_effective_month_year'
  )
  effective_year = fields.Integer(
    string = 'Effective year',
    store = True,
    readonly = True,
    index = True,
    compute = '_compute_revision_no_effective_month_year'
  )
  changes_count = fields.Integer(
    string = 'Changes count',
    readonly = True,
    default = 0,
    required = True,
  )
  
  employee_id = fields.Many2one(
    comodel_name = c.employee_model,
    string = 'Employee',
    index = True,
    required = True,
    ondelete = 'restrict', # TODO: need unit test
    readonly = True,
    store = True,
    related = 'contract_id.employee_id'
  )
  contract_id = fields.Many2one(
    comodel_name = c.contract_model,
    string = 'Contract',
    index = True,
    required = True,
    ondelete = 'restrict' # TODO: need unit test
  )
  department_id = fields.Many2one(
    comodel_name = c.department_model,
    string = 'Department',
    index = True,
    ondelete = 'restrict', # TODO: need unit test
  )
  job_id = fields.Many2one(
    comodel_name = c.job_model,
    string = 'Job Title',
    index = True,
    ondelete = 'restrict', # TODO: need unit test,
  )
  create_uid = fields.Many2one(
    comodel_name = c.users_model,
    string = 'Responsible',
    index = True,
    required = True,
    ondelete = 'restrict', # TODO: need unit test
    default = lambda self: self.env.user
  )
  previous_wage = fields.Float(
    string = 'Previous Payroll Wage',
    digits = (16, 2),
  )
  current_wage = fields.Float(
    string = 'Current Payroll Wage',
    digits = (16, 2),
    required = True, # TODO: need unit test
  )
  difference = fields.Float(
    string = 'Difference',
    digits = (16, 2),
    store = True,
    readonly = True,
    compute = '_compute_difference'
  )
  percentage = fields.Float(
    string = 'Percentage (%)',
    digits = (4, 2),
    store = True,
    readonly = True,
    compute = '_compute_difference'
  )
    
  @api.model
  def create(self, values):
    can_create_rule = self.env['hr.contract'].check_access_rights('create') #or self.env['hr.contract'].check_access_rights('edit')
    if not can_create_rule:#self.env.user.has_group('hr.manager'):
      raise UserError(_('You are not authorized to create Payroll Wage History'))
    return super(PayrollWageHistory, self).create(values)

      
  @api.depends(c.previous_wage_field, c.current_wage_field)
  def _compute_difference(self):
    for payroll_wage_history in self:
      payroll_wage_history.difference = utils.calculate_difference(payroll_wage_history)
      if not payroll_wage_history.previous_wage:
        payroll_wage_history.percentage = 0
        continue
      payroll_wage_history.percentage = utils.calculate_percentage(payroll_wage_history)
    return
  
  @api.depends(c.effective_date_field)
  def _compute_revision_no_effective_month_year(self):
    for payroll_wage_history in self:
      changes_count = payroll_wage_history.changes_count
      contract_ref = payroll_wage_history.contract_id.name
      effective_year = payroll_wage_history.effective_date.year
      payroll_wage_history.revision = utils.calculate_revision(
        c.revision_format,
        contract_ref,
        changes_count,
        effective_year
      )
      payroll_wage_history.effective_month = utils.extract_month_from_date(str(payroll_wage_history.effective_date))
      payroll_wage_history.effective_year = utils.extract_year_from_date(str(payroll_wage_history.effective_date))
    return