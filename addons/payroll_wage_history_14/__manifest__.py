# -*- coding: utf-8 -*-
{
    'name': "THD - Payroll Wage History for Odoo 12",  # Module title
    'summary': "Manage payroll wage history for Odoo 12",  # Module subtitle phrase
    'description': """
Manage Payroll Wage History for Odoo 12
==============
Description related to library.
    """,  # Supports reStructuredText(RST) format
    'author': "Truong Hoang Dung",
    'website': "https://github.com/revskill10",
    'category': 'HR',
    'version': '12',
    'depends': ['base', 'hr_contract'],
    # This data files will be loaded at the installation (commented because file is not added in this example)
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/payroll_wage_history_views.xml',
        'views/hr_contract_views.xml',
        #'views/hr_employee_views.xml',
        'report/report_salary_adjustment_form.xml',
        'wizards/payroll_wage_history_excel_report_views.xml',
        'templates/report_salary_adjustment_form_template.xml',
        'demo/payroll_wage_history_demo.xml'
    ],
    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    #'demo': [
    #    'demo/payroll_wage_history_demo.xml'
    #],
}
