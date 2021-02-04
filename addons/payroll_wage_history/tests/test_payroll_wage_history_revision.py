from odoo.tests import common, tagged
from . import test_utils as t
@tagged('-at_install', 'post_install')
class TestPayrollWageHistoryRevision(common.TransactionCase):
  def test_pwh_revision(self):
    employee = t.create_test_employee(self)
    job = self.env[t.job_model].create({ t.name_field: t.faker.job() })
    contract = self.env[t.contract_model].create({ 
      t.name_field: t.faker.name(), 
      t.wage_field: t.wage, 
      t.job_field: job.id, 
      t.employee_field: employee.id 
    })
    last_pwh = t.get_latest(self, t.pwh_model)
    expected_changes_count = 0
    expected_contract_ref = contract.name
    expected_effective_year = last_pwh.effective_date.year
    revision = t.revision_format.format(
      contract_ref=expected_contract_ref,
      changes_count=expected_changes_count,
      effective_year=expected_effective_year
    )
    t.assert_equal(self, last_pwh.revision, revision)
