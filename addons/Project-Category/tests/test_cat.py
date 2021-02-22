from odoo.tests.common import TransactionCase

class TestCategory(TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        self.Category = self.env['project.category']
        self.cat_ode = self.Category.create({
            'name': 'Odoo Development'})
        return result

    def test_create(self):
        "Test Category are active by default"
        self.assertEqual(self.cat_ode.active, True)