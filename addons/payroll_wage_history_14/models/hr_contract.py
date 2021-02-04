from odoo import models, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class HrContract(models.Model):
    _inherit = 'hr.contract'

    @api.model
    def create(self, values):
        contracts = super(HrContract, self).create(values)
        created_contracts_values = []
        for contract in contracts:
            if contract.employee_id:
                employee_id = contract.employee_id
                department_id = contract.department_id
                if not department_id:
                    department_id = employee_id.department_id
                job_id = contract.job_id
                current_wage = contract.wage
                if current_wage > 0:
                    created_contracts_values.append({
                        'contract_id': contract.id,
                        'employee_id': employee_id.id,
                        'current_wage': current_wage,
                        'department_id': department_id.id,
                        'job_id': job_id.id,
                    })
        if len(created_contracts_values) > 0:
            self.env['payroll.wage.history'].create(created_contracts_values)
        return contracts

    def write(self, values):
        current_wage = values.get('wage')
        job_id = values.get('job_id')
        department_id = values.get('department_id')
        if current_wage:
            updated_contracts_values = []
            for contract in self:
                previous_wage = contract.wage
                if float_compare(current_wage, previous_wage, 2) != 0:
                    employee_id = contract.employee_id
                    if not job_id:
                        job_id = contract.job_id.id
                    if not department_id:
                        department_id = contract.department_id.id
                    current_changes_count = self.env['payroll.wage.history'].search_count([
                        ('employee_id', '=', employee_id.id),
                        ('contract_id', '=', contract.id)
                    ])
                    updated_contracts_values.append({
                        'changes_count': current_changes_count,
                        'contract_id': contract.id,
                        'employee_id': employee_id.id,
                        'current_wage': current_wage,
                        'department_id': department_id,
                        'job_id': job_id,
                        'previous_wage': previous_wage,
                    })
            if len(updated_contracts_values) > 0:
                self.env['payroll.wage.history'].create(
                    updated_contracts_values)
        return super(HrContract, self).write(values)

    def get_salary_adjustment_form(self):
        domain = [('contract_id', '=', self.id)]
        wage_history = self.env['payroll.wage.history'].search(
                domain, order='id desc', limit=1)
        if wage_history and wage_history.previous_wage == 0:
            raise UserError(
                _('This contract is a new contract, you cannot get a salary adjustment form!'))
        else:
            if wage_history:
                return self.env.ref('payroll_wage_history_14.salary_adjustment_form').report_action(wage_history)
            else:
                raise UserError(_('This contract has no wage history record!'))
