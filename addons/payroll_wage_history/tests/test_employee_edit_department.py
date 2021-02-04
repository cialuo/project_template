from odoo.tests import common, tagged
from . import test_utils as t
@tagged('-at_install', 'post_install')
class TestEmployee(common.TransactionCase):
  def test_department_id_does_not_update_when_update_employee_department(self):
    employee = t.create_test_employee(self)
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id, 
      t.employee_field: employee.id 
    })
    last_pwh = t.get_latest(self, t.pwh_model)
    count_1 = self.env[t.pwh_model].search(
      [(t.employee_field, '=', employee.id)], 
      count = True
    )
    department_id = last_pwh.department_id
    t.assert_equal(self, employee.department_id.id, department_id.id)
    # Now we update employee's department
    department_2 = self.env[t.department_model].create({ t.name_field: t.faker.name() })
    employee.write({ t.department_field: department_2.id })
    # We assert last_pwh's department_id should not be changed
    last_pwh_2 = t.get_latest(self, t.pwh_model)
    t.assert_not_equal(self, last_pwh_2.department_id, department_2)
    t.assert_equal(self, last_pwh_2.department_id, department_id)
    t.assert_equal(self, last_pwh.revision, last_pwh_2.revision)
    count_2 = self.env[t.pwh_model].search(
      [(t.employee_field, '=', employee.id)], 
      count = True
    )
    t.assert_equal(self, count_1, count_2)