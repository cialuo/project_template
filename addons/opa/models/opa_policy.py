from odoo import models, fields, api, _
from opa_client.opa import OpaClient
def sync_opa(obj):
    client = OpaClient(host='opa') # default host='localhost', port=8181, version='v1'
    client.update_opa_policy_fromstring(obj['policy'], obj['name'])
    del client
    
class OpaPolicy(models.Model):
    _name="opa.policy"
    
    name = fields.Char(string="Name", required=True)
    policy = fields.Text(string="Policy", required=True)
    description = fields.Text(string="Description")
    
    _sql_constraints = [
        ('name', 'unique(name)', _('Please enter Unique Name')),
    ]
    
    @api.model
    def create(self, values):
        policies = super(OpaPolicy, self).create(values)
        self.env['opa.policy'].with_delay().sync_opa(values)
        return policies
    
    def write(self, values):
        name = self.name
        res = super(OpaPolicy, self).write(values)
        self.env['opa.policy'].with_delay().sync_opa({
            'name': name,
            'policy': values.get('policy')
        })
        for record in self:
            self._event('on_policy_updated').notify(record)
        return res
    
    def sync_opa_policies(self):
        for rec in self:
            self.env['opa.policy'].with_delay().sync_opa({
                'name': rec.name,
                'policy': rec.policy
            })
            
    @api.model
    def sync_opa(self, obj):
        client = OpaClient(host='opa') # default host='localhost', port=8181, version='v1'
        client.update_opa_policy_fromstring(obj['policy'], obj['name'])
        del client