# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import content_disposition, request
from odoo.addons.web.controllers.main import _serialize_exception
from odoo.tools import html_escape

import json


class OdooReportController(http.Controller):
    @http.route('/wage_history_reports', type='http', auth='user', methods=['GET'], csrf=False)
    # def get_report(self, model, options, output_format, financial_id=None, **kw):
    def get_report(self, report_id, **kw):
        output_format = 'xlsx'
        model = 'payroll.wage.history.excel.report'
        options = {'report_id': report_id}
        report_obj = request.env[model].sudo()
        report_name = 'Payroll Wage History Summary'
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition',
                         content_disposition(report_name + '.xlsx'))
                    ]
                )
                report_obj.get_xlsx(options, response)
            return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))
