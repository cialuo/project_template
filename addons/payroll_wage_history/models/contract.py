from odoo import models, api
from .. import constants as c
class HrContract(models.Model):
  _inherit = c.contract_model

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
            c.contract_field: contract.id,
            c.employee_field: employee_id.id,
            c.current_wage_field: current_wage,
            c.department_field: department_id.id,
            c.job_field: job_id.id,
          })
    if len(created_contracts_values) > 0:
      self.env[c.pwh_model].create(created_contracts_values)
    return contracts

  def write(self, values):
    current_wage = values.get(c.wage_field)
    job_id = values.get(c.job_field)    
    department_id = values.get(c.department_field)
    if current_wage:
      updated_contracts_values = []
      for contract in self:
        previous_wage = contract.wage
        if abs(current_wage - previous_wage) > 0.001:
          employee_id = contract.employee_id
          if not job_id:
            job_id = contract.job_id.id
          if not department_id:
            department_id = contract.department_id.id
          current_changes_count = self.env[c.pwh_model].search_count([
            (c.employee_field, '=', employee_id.id),
            (c.contract_field, '=', contract.id)
          ])
          updated_contracts_values.append({
            c.changes_count: current_changes_count,
            c.contract_field: contract.id,
            c.employee_field: employee_id.id,
            c.current_wage_field: current_wage,
            c.department_field: department_id,
            c.job_field: job_id,
            c.previous_wage_field: previous_wage,
          })
      if len(updated_contracts_values) > 0:
        self.env[c.pwh_model].create(updated_contracts_values)
    return super(HrContract, self).write(values)
