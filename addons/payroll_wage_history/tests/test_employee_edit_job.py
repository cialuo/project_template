from odoo.tests import common, tagged
from . import test_utils as t
@tagged('-at_install', 'post_install')
class TestEmployee(common.TransactionCase):
  def test_change_job_for_contract(self):
    employee = t.create_test_employee(self)
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    contract = self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id, 
      t.employee_field: employee.id 
    })
    job_2 = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    contract.write({ t.job_field: job_2.id, t.wage_field: t.wage_2, t.department_field: employee.department_id.id })
    pwh_2 = t.get_latest(self, t.pwh_model)
    t.assert_equal(self, pwh_2.job_id.id, job_2.id)
  def test_job_create_when_create_contract(self):
    employee = t.create_test_employee(self)
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    contract = self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id, 
      t.employee_field: employee.id 
    })
    last_pwh = t.get_latest(self, t.pwh_model)
    t.assert_equal(self, job.name, last_pwh.job_id.name)
  def test_job_id_does_not_update_when_update_contract_job_id(self):
    employee = t.create_test_employee(self)
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    contract = self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id, 
      t.employee_field: employee.id 
    })
    last_pwh = t.get_latest(self, t.pwh_model)
    job_id = last_pwh.job_id
    t.assert_equal(self, contract.job_id.id, job_id.id)
    # Now we update 
    job_2 = self.env[t.job_model].create({ t.name_field: t.faker.name() })
    contract.write({ t.job_field: job_2.id, t.job_field: job.id, t.department_field: employee.department_id.id })
    t.assert_equal(self, self.env[t.pwh_model].search_count([]), t.one)
    