from odoo.tests import common, tagged
from odoo import tools
from . import test_utils as t
@tagged('-at_install', 'post_install')
class TestTranslation(common.TransactionCase):
  def test_translate_company_title(self):
    tools.config.__setitem__('language', 'en_US, vi_VN')
    # create vietnamese
    langs = self.env['res.lang'].with_context(active_test=False).search([('code', '=', 'vi_VN')])
    langs.write({ 'active': True })
    print('langs', langs)
    domain = []# [('name', '=', 'hr_company,name')]
    trans = self.env['ir.translation'].search(domain)
    print('trans', trans)
    print('all languages', self.env['ir.translation']._get_languages())
    lang = self.env['res.lang'].search_read([])[0]
    print('lang', lang)