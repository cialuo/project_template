from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class PayrollWageHistory(models.Model):
    _name = 'payroll.wage.history'
    _description = 'Payroll Wage History'
    _rec_name = 'revision'

    revision = fields.Char(
        string='Revision No.',
        store=True,
        readonly=True,
        index=True,
        compute='_compute_revision_no_effective_month_year',
    )

    effective_date = fields.Date(
        string='Effective date',
        default=lambda self: fields.Date.today(),
        readonly=True,
    )
    effective_month = fields.Integer(
        string='Effective month',
        store=True,
        readonly=True,
        index=True,
        compute='_compute_revision_no_effective_month_year'
    )
    effective_year = fields.Integer(
        string='Effective year',
        store=True,
        readonly=True,
        index=True,
        compute='_compute_revision_no_effective_month_year'
    )
    changes_count = fields.Integer(
        string='Changes count',
        readonly=True,
        default=0,
        required=True,
    )

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        index=True,
        required=True,
        ondelete='restrict',  # TODO: need unit test
        readonly=True,
        store=True,
        related='contract_id.employee_id'
    )
    contract_id = fields.Many2one(
        comodel_name='hr.contract',
        string='Contract',
        index=True,
        required=True,
        ondelete='restrict'  # TODO: need unit test
    )
    department_id = fields.Many2one(
        comodel_name='hr.department',
        string='Department',
        index=True,
        ondelete='restrict',  # TODO: need unit test
    )
    job_id = fields.Many2one(
        comodel_name='hr.job',
        string='Job Title',
        index=True,
        ondelete='restrict',  # TODO: need unit test,
    )
    create_uid = fields.Many2one(
        comodel_name='res.users',
        string='Responsible',
        index=True,
        required=True,
        ondelete='restrict',  # TODO: need unit test
        default=lambda self: self.env.user
    )
    previous_wage = fields.Float(
        string='Previous Payroll Wage',
        digits=(16, 2),
    )
    current_wage = fields.Float(
        string='Current Payroll Wage',
        digits=(16, 2),
        required=True,  # TODO: need unit test
    )
    difference = fields.Float(
        string='Difference',
        digits=(16, 2),
        store=True,
        readonly=True,
        compute='_compute_difference'
    )
    percentage = fields.Float(
        string='Percentage (%)',
        digits=(4, 2),
        store=True,
        readonly=True,
        compute='_compute_difference'
    )

    @api.model
    def create(self, values):
        can_create_rule = self.env['hr.contract'].check_access_rights('create')
        if not can_create_rule:
            raise UserError(
                _('You are not authorized to create Payroll Wage History'))
        return super(PayrollWageHistory, self).create(values)

    @api.depends('previous_wage', 'current_wage')
    def _compute_difference(self):
        for payroll_wage_history in self:
            payroll_wage_history.difference = payroll_wage_history.current_wage - \
                payroll_wage_history.previous_wage
            if not payroll_wage_history.previous_wage:
                payroll_wage_history.percentage = 0
                continue
            payroll_wage_history.percentage = 100.0 * \
                (payroll_wage_history.current_wage -
                 payroll_wage_history.previous_wage) / payroll_wage_history.previous_wage
        return

    @api.depends('effective_date')
    def _compute_revision_no_effective_month_year(self):
        for payroll_wage_history in self:
            changes_count = payroll_wage_history.changes_count
            contract_ref = payroll_wage_history.contract_id.name
            effective_year = payroll_wage_history.effective_date.year
            payroll_wage_history.revision = '{contract_ref}-{changes_count}-{effective_year}'.format(
                contract_ref=contract_ref,
                changes_count=changes_count,
                effective_year=effective_year
            )
            payroll_wage_history.effective_month = int(datetime.strptime(
                str(payroll_wage_history.effective_date), '%Y-%m-%d').strftime('%m'))
            payroll_wage_history.effective_year = int(datetime.strptime(
                str(payroll_wage_history.effective_date), '%Y-%m-%d').strftime('%Y'))
        return

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self._context.get('highest_raise'):
            sel_sql = """
                SELECT max(percentage)
                FROM payroll_wage_history
                WHERE effective_date >= CURRENT_DATE - INTERVAL '365 DAYS';
            """
            self._cr.execute(sel_sql)
            highest_raise = self._cr.fetchone()[0]
            last_12_months = (datetime.now() + timedelta(days=-365)).date()
            args += ['&', ('percentage', '=', highest_raise),
                     ('effective_date', '>=', last_12_months)]

        if self._context.get('no_raise_in_12_months'):
            last_12_months = (datetime.now() + timedelta(days=-365)).date()
            args += [('difference', '>', 0), ('effective_date', '>=',
                                              last_12_months), ('changes_count', '>=', 1)]
            raised_employee_ids = super(PayrollWageHistory, self).search(
                args).mapped('employee_id.id')
            args = [('employee_id', 'not in', raised_employee_ids)]

        return super(PayrollWageHistory, self).search(args, offset=offset, limit=limit, order=order, count=count)
