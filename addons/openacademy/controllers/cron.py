from odoo import http
from odoo.http import request
import logging
import json
_logger = logging.getLogger(__name__)

class Todo(http.Controller):
    @http.route('/cron/test_odoo/', type='json', auth='public')
    def index(self, **kw):
        data = json.loads(request.httprequest.data)
        _logger.debug('abc %s', str(data['payload']['hello']))
        return {'hello': '1'}