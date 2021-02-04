# -*- coding: utf-8 -*-
{
    'name': "THD - Payroll Wage History",  # Module title
    'summary': "Manage payroll wage history",  # Module subtitle phrase
    'description': """
Manage Payroll Wage History
==============
Description related to library.
    """,  # Supports reStructuredText(RST) format
    'author': "Truong Hoang Dung",
    'website': "https://github.com/revskill10",
    'category': 'HR',
    'version': '14.0.1',
    'depends': ['base','hr_contract'],
    # This data files will be loaded at the installation (commented because file is not added in this example)
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml'
    ],
    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
}