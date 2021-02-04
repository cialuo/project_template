from odoo.tests import common, tagged
from . import test_utils as t
@tagged('-at_install', 'post_install')
class TestWageRaise(common.TransactionCase):
  def test_pwh_should_not_be_created_if_wage_not_changed(self):
    employee = t.create_test_employee(self)
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    contract = self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id, 
      t.employee_field: employee.id 
    })
    contract.write({ t.wage_field: t.wage })
    t.assert_equal(self, self.env[t.pwh_model].search_count([]), t.one)
    