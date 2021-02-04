from odoo.tests import common, tagged
from . import test_utils as t
@tagged('-at_install', 'post_install')
class TestEmployee(common.TransactionCase):
  def test_employee_pwh_count_is_zero_without_contract(self):
    employee = t.create_test_employee(self)
    t.assert_equal(self, employee.wage_history_rec_count, t.zero)
    
  def test_employee_count_change_when_pwh_created(self):
    employee = t.create_test_employee(self)
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    contract = self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id, 
      t.employee_field: employee.id 
    })
    t.assert_equal(self, self.env[t.pwh_model].search_count([t.filter_by_employee(employee)]), t.one)
    t.assert_equal(self, employee.wage_history_rec_count, t.one)
    contract.write({ t.wage_field: t.wage_2, t.job_field: job.id, t.department_field: employee.department_id.id })
    contract.write({ t.wage_field: t.wage_3, t.job_field: job.id, t.department_field: employee.department_id.id })
    t.assert_equal(self, employee.wage_history_rec_count, t.three)
    
    