# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'White Attachment Mimetypes',
    'version': '0.1',
    'author': 'Tamkeen Technologies',
    'website': 'http://tamkeentech.sa/',
    'website': '',
    'description': """
Control the Attachments Mimetypes & Size:
##########################################
        - Allow to specify the type of the attachment extensions(e.g, PDF, DOCX, ...etc) that will be permitted to be uploaded by the system.
        - Allow also to specify the attachment maximum size (e.g, 10 MB) in the company definition.
    """,
    'depends': [
       'document',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'security/ir_rule.xml',
        'ir_attachment_view.xml',
        'white_mimetype_data.xml',
        'white_mimetype_view.xml',
        'res_company_view.xml',
    ],
    'active': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
