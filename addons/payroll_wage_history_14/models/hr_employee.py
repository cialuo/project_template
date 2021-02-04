from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    wage_history_rec_count = fields.Integer(
        string='Wage History Record(s)',
        compute='_count_wage_history_rec',
        default=0,
        store=True,
    )

    wage_ids = fields.One2many('payroll.wage.history', 'employee_id', string = 'Wage History')

    @api.depends('wage_ids')
    def _count_wage_history_rec(self):
        wage_history_env = self.env['payroll.wage.history']
        for employee in self:
            rec_count = wage_history_env.search(
                [('employee_id', '=', employee.id)],
                count=True
            )
            employee.wage_history_rec_count = rec_count
        return

    def get_payroll_wage_history(self):
        return {
            'name': 'Payroll Wage History for {employee}'.format(employee=self.name),
            'type': 'ir.actions.act_window',
            'res_model': 'payroll.wage.history',
            'view_mode': 'tree',
            'domain': [('employee_id', '=', self.id)],
            'target': 'new',
            'context': {'hide_employee': True, 'is_modal': True }
        }