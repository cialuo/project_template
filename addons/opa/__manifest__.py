# -*- coding: utf-8 -*-
{
    'name': "OPA",  # Module title
    'summary': "Manage OPA",  # Module subtitle phrase
    'description': """
Manage OPA
==============
Description related to OPA.
    """,  # Supports reStructuredText(RST) format
    'author': "Truong Hoang Dung",
    'website': "http://www.example.com",
    'category': 'Tools',
    'version': '14.0.1',
    'depends': ['base'],
    # This data files will be loaded at the installation (commented because file is not added in this example)
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/opa_policy.xml'
    ],
    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
}
