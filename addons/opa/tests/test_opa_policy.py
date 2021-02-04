from odoo.tests import common, tagged
@tagged('-at_install', 'post_install')
class TestEmployee(common.TransactionCase):
    def test_effective_month_year(self):
        p = self.env['opa.policy'].with_context(test_queue_job_no_delay=True).create({
            'name': 'test1',
            'policy': 'abc',
            'description': 'xxx'
        })
        print('id %s', p.id)