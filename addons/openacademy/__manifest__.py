# -*- coding: utf-8 -*-
{
    'name': "Open Academy",  # Module title
    'summary': "Open Academy",  # Module subtitle phrase
    'description': """
Open Academy module for managing trainings:
            - training courses
            - training sessions
            - attendees registration
    """,  # Supports reStructuredText(RST) format
    'author': "Truong Hoang Dung",
    'website': "http://www.example.com",
    'category': 'Tools',
    'version': '14.0.1',
    'depends': ['base'],
    # This data files will be loaded at the installation (commented because file is not added in this example)
    'data': [
        'security/ir.model.access.csv',
        'views/course.xml',
        'views/session.xml',
        'views/partner.xml'
    ],
    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    #'demo': [
    #    'demo/course.xml'
    #],
}
