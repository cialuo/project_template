# -*- coding: utf-8 -*-
#from osv import osv, fields
from openerp.osv import fields, osv
from content_index import cntIndex
from openerp.tools.misc import ustr
from openerp.exceptions import Warning
from openerp import _

class ir_attachment(osv.Model):
    _inherit = 'ir.attachment'

    def _get_company(self,cr, uid, context=None, uid2=False):
        if not uid2:
            uid2 = uid
        user = self.pool.get('res.users').read(cr, uid, uid2, ['company_id'], context)
        company_id = user.get('company_id', False)
        return company_id and company_id[0] or False

    def _get_allowed_attachment_size(self, cr, uid, context=None):
        attachment_size = 10, # MB
        company_id = self._get_company(cr, uid, context)
        if company_id:
            attachment_size = self.pool.get('res.company').browse(cr, uid, company_id).attachment_size
        return attachment_size

    def _get_allowed_mimetype_id(self, cr, uid, context=None):
        mimetype_pool = self.pool.get('white.mimetype')
        ids = mimetype_pool.search(cr, uid, [('active','=','True')], context=context)
        result = [ (x.name) \
                for x in mimetype_pool.browse(cr, uid, ids, context=context) ]
        return result

    def is_allowed_attachment(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        attached_file_size = 0.0
        if values.get('datas'):
            attached_file_size = round((len(values['datas'].decode('base64')) / (1024 * 1024)) , 2) # Miga byte
        company_id = self._get_company(cr, uid, context)
        company_allowed_size = self._get_allowed_attachment_size(cr, uid, context) #10 # MB
        if company_allowed_size and attached_file_size <= company_allowed_size: 
            return True
        else:
            return False

    def _index(self, cr, uid, data, datas_fname, file_type):
        mime, icont = cntIndex.doIndex(data, datas_fname,  file_type or None, None)
        icont_u = ustr(icont)
        return mime , icont_u

    def write(self, cr, uid, ids, values, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]

        if self.is_allowed_attachment(cr, uid, values, context):
            if values.get('datas', False):
                values['file_type'], values['index_content'] = self._index(cr, uid, values['datas'].decode('base64') , values.get('datas_fname', False), None) #, vals['index_content'] = , vals.get('datas_fname', False), None)
            active_allowed_mimetypes = self._get_allowed_mimetype_id(cr, uid, context)
            if active_allowed_mimetypes:
                if values.get('file_type'):
                    if values['file_type'] and values['file_type'] in active_allowed_mimetypes:
                        self.check(cr, uid, ids, 'write', context=context, values=values)
                        if 'file_size' in values:
                            del values['file_size']
                        return super(ir_attachment, self).write(cr, uid, ids, values, context)
                    else:
                        # raise Warning(_("Please upload a supported file format by the system('e.g pdf or word file')"))
                        raise osv.except_osv("Upload Restriction","Please upload a supported file format by the system('e.g pdf or word file')") 
            else:
                # raise Warning(_("Please define the system allowed mimetypes or contact your system admin"))
                raise osv.except_osv("Not Defined Mimetypes","Please define the system allowed mimetypes or contact your system admin") 
        else:
            # raise Warning(_("The attachment size must be less than 10 MB."))
            raise osv.except_osv("Size Exceeded","The attachment size must be less than 10 MB.") 

    def create(self, cr, uid, values, context=None):
        if context is None:
            context = {}

        if values.get('datas_fname', False):
            if self.is_allowed_attachment(cr, uid, values, context):      
                if values.get('datas', False):
                    values['file_type'], values['index_content'] = self._index(cr, uid, values['datas'].decode('base64') , values.get('datas_fname', False), None) #, vals['index_content'] = , vals.get('datas_fname', False), None)
                
                active_allowed_mimetypes = self._get_allowed_mimetype_id(cr, uid, context)
                if active_allowed_mimetypes:
                    if values['file_type'] and values['file_type'] in active_allowed_mimetypes:
                        self.check(cr, uid, [], mode='write', context=context, values=values)
                        if 'file_size' in values:
                            del values['file_size']
                        return super(ir_attachment, self).create(cr, uid, values, context)   
                    else:
                        # raise Warning(_("Please upload a supported file format by the system('e.g pdf or word file')"))
                        raise osv.except_osv("Upload Restriction","Please upload a supported file format by the system('e.g pdf or word file')") 
                else:
                    # raise Warning(_("Please define the system allowed mimetypes or contact your system admin"))
                    raise osv.except_osv("Not Defined Mimetypes","Please define the system allowed mimetypes or contact your system admin") 
            else:
                # raise Warning(_("The attachment size must be less than 10 MB."))
                raise osv.except_osv("Size Exceeded","The attachment size must be less than 10 MB.") 

ir_attachment()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
