from odoo.tests import common, tagged
from . import test_utils as t
@tagged('-at_install', 'post_install')
class TestWageRaise(common.TransactionCase):
  @t.raise_access_error
  def test_user_should_be_able_to_create_contract(self):
    groups = self.env['res.groups'].search([('name', '=', 'Public')])
    public_groups_id = groups.mapped('id')
    hr_officer = self.env['res.users'].create({
      'login': 'testuser',
      'partner_id': self.env['res.partner'].create({
          'name': "Strawman Test User"
        }).id,
      'groups_id': public_groups_id
    })
    self.env['payroll.wage.history'].sudo(hr_officer.id).create({})
  @t.raise_integrity_error
  def test_user_should_be_able_to_create_contract(self):
    group = self.env['res.groups'].create({ 'name': 'Contracts/Administrator' })
    groups_id = [group.id]
    model_id = self.env['ir.model'].search([('name', '=', 'Contract')])
    self.env['ir.model.access'].create({
      'name': 'Contracts Manager',
      'model_id': model_id.id,
      'group_id': group.id,
      'perm_read': True,
      'perm_write': True,
      'perm_create': True,
      'perm_unlink': True,
    })
    hr_officer = self.env['res.users'].create({
      'login': 'testuser',
      'partner_id': self.env['res.partner'].create({
          'name': "Strawman Test User"
        }).id,
      'groups_id': groups_id
    })
    self.env['payroll.wage.history'].sudo(hr_officer.id).create({})
