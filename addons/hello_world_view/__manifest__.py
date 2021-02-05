# -*- coding: utf-8 -*-
{
    'name': "Hello world view",  # Module title
    'summary': "Hello world view",  # Module subtitle phrase
    'description': """
Manage OPA
==============
Description related to OPA.
    """,  # Supports reStructuredText(RST) format
    'author': "Truong Hoang Dung",
    'website': "http://www.example.com",
    'category': 'Tools',
    'version': '14.0.1',
    'depends': ['web', 'contacts', 'base_geolocalize'],
    # This data files will be loaded at the installation (commented because file is not added in this example)
    'data': [
        "views/assets.xml",
        "views/data.xml"
    ],
    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
    'qweb': ['static/src/xml/hello_world_view.xml'],
    'installable': True,
    'auto_install': True,
}
