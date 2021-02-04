import io
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta, date
import logging
_logger = logging.getLogger(__name__)
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    # TODO saas-17: remove the try/except to directly import from misc
    import xlsxwriter


class PayrollWageHistoryExcelReport(models.TransientModel):
    _name = 'payroll.wage.history.excel.report'

    from_date = fields.Date(
        string="From Date", default=lambda self: (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d'))
    to_date = fields.Date(string="To Date", default=fields.Date.context_today)
    department_id = fields.Many2one(
        comodel_name='hr.department',
        string='Department',
    )
    job_id = fields.Many2one(
        comodel_name='hr.job',
        string='Job Title',
    )
    data = fields.Binary('File', readonly=True)
    name = fields.Char('File name')
    ORDER_BY = [
        ('p.current_wage desc', 'Current Wage (Desc)'),
        ('p.percentage desc', 'Percentage (Desc)'),
        ('p.effective_date desc', 'Effective Date (Desc)'),
    ]
    order_by = fields.Selection(ORDER_BY, default=ORDER_BY[0][0])
    employee_ids = fields.Many2many('hr.employee', string='Employee(s)')

    def set_cw(self, sheet, column, x):
        cw = column.get('cw', 16)
        if cw:
            sheet.set_column(x, x, cw)

    def download_report(self):
        # raise UserError('test loi thu')
        return {
            'type': 'ir.actions.act_url',
            # 'url': '/helpdesk/ticket/%s' % self.id,
            'url': '/wage_history_reports?report_id=%s' % self.id,
            'target': 'new',
            'res_id': self.id,
        }

    def get_style(self, workbook):
        def_style = workbook.add_format({'font_name': 'Arial'})
        title_style = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'bottom': 2})
        super_col_style = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'align': 'center'})
        level_0_style = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'bottom': 2, 'top': 2, 'pattern': 1, 'font_color': '#FFFFFF'})
        level_0_style_left = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'bottom': 2, 'top': 2, 'left': 2, 'pattern': 1, 'font_color': '#FFFFFF'})
        level_0_style_right = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'bottom': 2, 'top': 2, 'right': 2, 'pattern': 1, 'font_color': '#FFFFFF'})
        level_1_style = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'bottom': 2, 'top': 2})
        level_1_style_left = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'bottom': 2, 'top': 2, 'left': 2})
        level_1_style_right = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'bottom': 2, 'top': 2, 'right': 2})
        level_2_style = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'top': 2})
        level_2_style_left = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'top': 2, 'left': 2})
        level_2_style_right = workbook.add_format(
            {'font_name': 'Arial', 'bold': True, 'top': 2, 'right': 2})
        level_3_style = def_style
        level_3_style_left = workbook.add_format(
            {'font_name': 'Arial', 'left': 2})
        level_3_style_right = workbook.add_format(
            {'font_name': 'Arial', 'right': 2})
        domain_style = workbook.add_format(
            {'font_name': 'Arial', 'italic': True})
        domain_style_left = workbook.add_format(
            {'font_name': 'Arial', 'italic': True, 'left': 2})
        domain_style_right = workbook.add_format(
            {'font_name': 'Arial', 'italic': True, 'right': 2})
        upper_line_style = workbook.add_format(
            {'font_name': 'Arial', 'top': 2})
        bold_h_left_v_center = workbook.add_format({'font_name': 'Arial', 'bold': True,
                                                    'align': 'left', 'valign': 'vcenter'})
        account_style_h_left_v_top = workbook.add_format(
            {'font_name': 'Arial', 'italic': True, 'font_size': 8, 'align': 'left', 'valign': 'top'})
        style_xl = {
            'def_style':  def_style,
            'title_style': title_style,
            'super_col_style': super_col_style,
            'level_0_style': level_0_style,
            'level_0_style_left': level_0_style_left,
            'level_0_style_right': level_0_style_right,
            'level_1_style': level_1_style,
            'level_1_style_left': level_1_style_left,
            'level_1_style_right': level_1_style_right,
            'level_2_style': level_2_style,
            'level_2_style_left': level_2_style_left,
            'level_2_style_right': level_2_style_right,
            'level_3_style': level_3_style,
            'level_3_style_left': level_3_style_left,
            'level_3_style_right': level_3_style_right,
            'domain_style': domain_style,
            'domain_style_left': domain_style_left,
            'domain_style_right': domain_style_right,
            'upper_line_style': upper_line_style,
            'bold_h_left_v_center': bold_h_left_v_center,
            'account_style_h_left_v_top': account_style_h_left_v_top
        }
        return style_xl

    def super_columns_style(self, workbook):
        super_col_def_style = workbook.add_format({'font_name': 'Arial'})
        report_name_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 20,
                                                 'align': 'center', 'valign': 'vcenter'})
        account_style = workbook.add_format(
            {'font_name': 'Arial', 'italic': True, 'font_size': 8, 'align': 'center', 'valign': 'vcenter'})

        super_col_styles = {'super_col_def_style': super_col_def_style,
                            'report_name_style': report_name_style,
                            'account_style': account_style
                            }
        return super_col_styles

    def get_style_update(self, workbook):
        title_style = workbook.add_format({'font_name': 'Arial', 'bold': True,
                                           'text_wrap': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#d8dee8',
                                           'top': 1, 'left': 1, 'bottom': 1, 'right': 1})
        level_2_style = workbook.add_format(
            {'font_name': 'Arial', 'bold': False, 'top': 1, 'left': 1, 'bottom': 1, 'right': 1})
        level_2_style_left = workbook.add_format(
            {'font_name': 'Arial', 'bold': False, 'top': 1, 'left': 1, 'bottom': 1, 'right': 1})
        level_2_style_right = workbook.add_format(
            {'font_name': 'Arial', 'bold': False, 'top': 1, 'left': 1, 'bottom': 1, 'right': 1})

        def_style = workbook.add_format(
            {'font_name': 'Arial', 'top': 1, 'left': 1, 'bottom': 1, 'right': 1})

        level_3_style = workbook.add_format(
            {'font_name': 'Arial', 'top': 1, 'left': 1, 'bottom': 1, 'right': 1})
        level_3_style_left = workbook.add_format(
            {'font_name': 'Arial', 'top': 1, 'left': 1, 'bottom': 1, 'right': 1})
        level_3_style_right = workbook.add_format(
            {'font_name': 'Arial', 'top': 1, 'left': 1, 'bottom': 1, 'right': 1})

        return {
            'title_style': title_style,
            'level_2_style': level_2_style,
            'level_2_style_left': level_2_style_left,
            'level_2_style_right': level_2_style_right,
            'level_3_style': level_3_style,
            'level_3_style_left': level_3_style_left,
            'level_3_style_right': level_3_style_right,
            'def_style': def_style
        }

    def write_header(self, sheet, y_offset, header_columns, style_xl):
        is_merge_title = False
        for h in header_columns:
            if h.get('column_fist_merge'):
                is_merge_title = True

        title_style = style_xl['title_style']
        x = 0
        if is_merge_title:
            range_merge_x = -1
            for column in header_columns:  # ghi header
                column_fist_merge = column.get('column_fist_merge')
                if column_fist_merge:
                    range_merge_x = x + column.get('width_merge_tilte')
                    sheet.merge_range(y_offset, x, y_offset, x + column.get(
                        'width_merge_tilte')-1, column_fist_merge, title_style)
                    sheet.write(y_offset+1, x, column.get('name', '').replace(
                        '<br/>', ' ').replace('&nbsp;', ' '), title_style)
                else:
                    if x <= range_merge_x:
                        sheet.write(y_offset+1, x, column.get('name', '').replace(
                            '<br/>', ' ').replace('&nbsp;', ' '), title_style)
                    else:
                        sheet.merge_range(y_offset, x, y_offset + 1, x, column.get(
                            'name', '').replace('<br/>', ' ').replace('&nbsp;', ' '), title_style)

                self.set_cw(sheet, column, x)

                x += 1

            return y_offset + 1

        else:
            for column in header_columns:
                sheet.write(y_offset, x, column.get('name', '').replace(
                    '<br/>', ' ').replace('&nbsp;', ' '), title_style)
                self.set_cw(sheet, column, x)
                x += 1
            return y_offset

    def get_columns_name(self, options):
        return [{'name': _("Department"), 'cw': 20},
                {'name': _("Job title"), 'cw': 20},
                {'name': _("Employee"), 'cw': 20},
                {'name': _("Current wage"), 'cw': 20},
                {'name': _("Previous Wage"), 'cw': 20},  # sửa thành nguyên tệ

                {'name': _('Raise (%)'), 'cw': 20},
                {'name': _('Effective months'), 'cw': 20},
                ]

    def get_xlsx(self, options, response):
        report = self.env['payroll.wage.history.excel.report'].browse(
            int(options['report_id']))

        # ctx = self.set_context(options)
        ctx = {}
        ctx.update({'no_format': True, 'print_mode': True,
                    'prefetch_fields': False})
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        # report_name_new = self.get_report_name_new(options)#[:31]
        report_name_new = 'Wage History Summary'
        sheet = workbook.add_worksheet(report_name_new)
        header_columns = self.with_context(ctx).get_columns_name(options)
        # len_header_columns = len(header_columns)
        style_xl = self.get_style(workbook)
        style_xl.update(self.get_style_update(workbook))

        ###############
        # self.set_col_width(sheet)
        # đưa report_name vào đây luôn
        y_offset = 0
        # super_columns_list = self._super_columns_list( workbook, options, ctx, report_name_new, len_header_columns)

        # y_offset = self._ndt_write_super_columns(workbook, super_columns_list, sheet, y_offset)

        y_offset = self.write_header(sheet, y_offset, header_columns, style_xl)
        # y_offset +=1
        # x = 0
        # for column in header_columns: # ghi header
        #     sheet.write(y_offset, x, column.get('name', '').replace('<br/>', ' ').replace('&nbsp;', ' '), title_style)
        #     cw = column.get('cw', self.default_cw)
        #     if cw:
        #         sheet.set_column(x, x, cw)
        #     x += 1
        domain = [
            ('create_date', '>=', report.from_date),
            ('create_date', '<=', report.to_date),
        ]
        if len(report.employee_ids.ids) > 0:
            domain.append(('employee_id', 'in', report.employee_ids.ids))
        if report.department_id:
            domain.append(('department_id', '=', report.department_id.id))
        if report.job_id:
            domain.append(('job_id', '=', report.job_id.id))
        can_read = self.env['payroll.wage.history'].check_access_rights('read')
        if not can_read:
            raise UserError(_('You are not authorized to read Payroll Wage History Report'))
        query = self.env['payroll.wage.history']._where_calc(domain)
        self.env['payroll.wage.history']._apply_ir_rules(query, 'read')
        _, where, where_params = query.get_sql()
        where = where.replace('payroll_wage_history', 'p')
        if where:
            where = 'and %(where)s' % {'where': where}
        order_by = ''
        if report.order_by:
            order_by = 'order by %(order_by)s' % {'order_by': report.order_by}
        sql_string = """with tmp1 as (
select p.*, e.name as employee_name, hd.name as department_name, j.name as job_title
from payroll_wage_history p
inner join hr_employee e on e.id = p.employee_id
inner join hr_department hd on hd.id = p.department_id
inner join hr_job j on j.id = p.job_id
where e.active = true
%(user_where_clause)s
%(order_by)s
)
SELECT
jsonb_object_agg(key, value) as result
FROM (
SELECT
    jsonb_build_object(department_name, jsonb_object_agg(key, value)) as departments
FROM (
    SELECT
        case department_name when NULL then 'undefined' else department_name end,
        jsonb_build_object(job_title, jsonb_agg(json_build_object(
                'employee_name', employee_name,
                'revision', revision,
                'current_wage', current_wage,
                'previous_wage', previous_wage,
                'raise', percentage,
                'effective_months', date_part('month', (SELECT current_timestamp)) - effective_month
            ))) AS job_title
    FROM tmp1
GROUP BY department_name, job_title
) s,
jsonb_each(job_title)

GROUP BY department_name
) s,
jsonb_each(departments)""" % {
            'user_where_clause': where,
            'order_by': order_by
        }
        self.env.cr.execute(sql_string, tuple(where_params))
        result = self.env.cr.dictfetchall()
        departments = result[0]['result']
        row = 0
        for department in departments.keys():
            row = row + 1
            sheet.write(row, 0, department)
            jobs = departments[department]
            for job in jobs.keys():
                row = row + 1
                sheet.write(row, 1, job)
                employees = jobs[job]
                for employee in employees:
                    row = row + 1
                    sheet.write(row, 2, employee['employee_name'])
                    sheet.write(row, 3, employee['current_wage'])
                    sheet.write(row, 4, employee['previous_wage'])
                    sheet.write(row, 5, employee['raise'])
                    sheet.write(row, 6, employee['effective_months'])
        workbook.close()
        output.seek(0)
        # return output
        response.stream.write(output.read())
        output.close()
