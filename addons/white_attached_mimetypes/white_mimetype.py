# -*- coding: utf-8 -*-

# from osv import osv, fields
from openerp.osv import fields, osv

class white_mimetype(osv.Model):
    _name = 'white.mimetype'

    _columns = {
        'name': fields.char('Name', required=True),
        'active': fields.boolean('Active'),
    }

    _sql_constraints = [
        ('uniq_white_mimetype_name', 'UNIQUE(name)', 'Name of mimetype must be unique !'),
    ]

white_mimetype()
