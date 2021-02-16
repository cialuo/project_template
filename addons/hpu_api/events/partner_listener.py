from odoo.addons.component.core import Component
import logging
_logger = logging.getLogger(__name__)
class MyEventListener(Component):
    _name = 'res.partner.listener'
    _inherit = 'base.event.listener'

    def on_res_partner_updated(self, record):
        _logger.debug('partner %s has been paid!', record.name)