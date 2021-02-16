from odoo.tests import common, tagged
@tagged('-at_install', 'post_install')
class TestWageRaise(common.TransactionCase):
  def test_pwh_should_not_be_created_if_wage_not_changed(self):
    self.assertEqual(1+1, 3)
    