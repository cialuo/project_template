from odoo.tests import common, tagged
from . import test_utils as t
from .. import utils
@tagged('-at_install', 'post_install')
class TestEmployee(common.TransactionCase):
  def test_effective_month_year(self):
    employee = t.create_test_employee(self)
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id, 
      t.employee_field: employee.id 
    })
    last_pwh = t.get_latest(self, t.pwh_model)
    t.assert_equal(self, utils.extract_month_from_date(str(last_pwh.effective_date)), last_pwh.effective_month)
    t.assert_equal(self, utils.extract_year_from_date(str(last_pwh.effective_date)), last_pwh.effective_year)
    