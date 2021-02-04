# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class PayrollWageHistoryReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.payroll_wage_history_14.salary_adjustment_form'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['payroll.wage.history'].browse(docids)
        _logger.info('pwh', docs)
        return {
            'docs': docs,
        }
