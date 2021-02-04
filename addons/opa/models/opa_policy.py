from odoo import models, fields, api, _
from opa_client.opa import OpaClient
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
def sync_opa(obj):
    client = OpaClient(host='opa') # default host='localhost', port=8181, version='v1'
    client.update_opa_policy_fromstring(obj['policy'], obj['name'])
    del client
    
class OpaPolicy(models.Model):
    _name="opa.policy"
    
    name = fields.Char(string="Name", required=True)
    policy = fields.Text(string="Policy")
    description = fields.Text(string="Description")
    
    _sql_constraints = [
        ('name', 'unique(name)', _('Please enter Unique Name')),
    ]
    
    @api.model
    def create(self, values):
        policies = super(OpaPolicy, self).create(values)
        sync_opa(values)
        return policies
    
    def write(self, values):
        res = super(OpaPolicy, self).write(values)
        sync_opa(values)
        return res