from odoo.addons.component.core import Component
import logging
_logger = logging.getLogger(__name__)

class MyEventListener(Component):
    _name = 'my.event.listener'
    _inherit = 'base.event.listener'

    def on_policy_updated(self, record):
        _logger.debug('invoice %s has been paid!', record.name)