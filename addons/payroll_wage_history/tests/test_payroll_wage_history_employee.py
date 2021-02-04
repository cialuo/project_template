from odoo.tests import common, tagged
from . import test_utils as t
@tagged('-at_install', 'post_install')
class TestEmployee(common.TransactionCase):
  @t.raise_integrity_error
  def test_pwh_cannot_exist_without_employee(self):
    self.env[t.pwh_model].create({})
    
  def test_no_pwh_without_employee(self):
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id 
    })
    t.assert_equal(self, self.env[t.pwh_model].search_count([]), t.zero)
    
  def test_one_pwh_created_with_one_new_contract(self):
    employee = t.create_test_employee(self)
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id, 
      t.employee_field: employee.id 
    })
    t.assert_equal(self, self.env[t.pwh_model].search_count([]), t.one)
    
  def test_pwh_difference_with_one_new_contract(self):
    employee = t.create_test_employee(self)
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id, 
      t.employee_field: employee.id 
    })
    last_pwh = t.get_latest(self, t.pwh_model)
    t.assert_equal(self, last_pwh.difference, t.wage)
    
  def test_pwh_percentage_with_updated_contract(self):
    employee = t.create_test_employee(self)
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    contract = self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id, 
      t.employee_field: employee.id 
    })
    contract.write({ t.wage_field: t.wage_2, t.job_field: job.id, t.department_field: employee.department_id.id })
    expected_percentage = 100.0 * (t.wage_2 - t.wage) / t.wage
    last_pwh = t.get_latest(self, t.pwh_model)
    t.assert_equal(self, last_pwh.percentage, expected_percentage)
    
  def test_two_pwh_created_with_two_new_contracts_for_same_employee(self):
    employee = t.create_test_employee(self)
    job1 = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    job2 = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job1.id, 
      t.employee_field: employee.id 
    })
    self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job2.id, 
      t.employee_field: employee.id 
    })
    t.assert_equal(self, self.env[t.pwh_model].search_count([t.filter_by_employee(employee)]), t.two)
  
  def test_two_pwh_created_with_two_new_contracts_for_two_employees(self):
    employee_1 = t.create_test_employee(self)
    employee_2 = t.create_test_employee(self)
    job1 = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    job2 = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(),
      t.wage_field: t.wage, 
      t.job_field: job1.id, 
      t.employee_field: employee_1.id 
    })
    self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job2.id, 
      t.employee_field: employee_2.id 
    })
    t.assert_equal(self, self.env[t.pwh_model].search_count([t.filter_by_employee(employee_1)]), t.one)
    t.assert_equal(self, self.env[t.pwh_model].search_count([t.filter_by_employee(employee_2)]), t.one)
  
  def test_pwh_updated_with_employee(self):
    employee = t.create_test_employee(self)
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    contact = self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id, 
      t.employee_field: employee.id 
    })
    contact.write({ t.wage_field: t.wage_2, t.job_field: job.id, t.department_field: employee.department_id.id })
    t.assert_equal(self, self.env[t.pwh_model].search_count([t.filter_by_employee(employee)]), t.two)
    
  def test_pwh_should_not_be_updated_without_wage_changes(self):
    employee = t.create_test_employee(self)
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    contact = self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id, 
      t.employee_field: employee.id 
    })
    contact.write({ t.wage_field: t.wage_2, t.job_field: job.id, t.department_field: employee.department_id.id })
    contact.write({ t.wage_field: t.wage_3, t.job_field: job.id, t.department_field: employee.department_id.id })
    t.assert_equal(self, self.env[t.pwh_model].search_count([]), t.three)
    