from odoo import api, models


def create_with_xml_id(self, model, vals):
    module = 'payroll_wage_history_demo'
    xml_id = vals.pop('xml_id')
    model_name = model.replace('.', '_')
    name = "%s_%s_%s" % (module, model_name, xml_id)
    xml_rec = self.env['ir.model.data'].search(
        [('name', '=', name)], limit=1, order='id desc')
    rec = None
    is_new = False
    if not xml_rec:
        rec = self.env[model].create(vals)
        self.env["ir.model.data"].create({
            'name': name,
            'res_id': rec.id,
            'model': model,
            'module': module
        })
        is_new = True
    else:
        rec = self.env[model].search([('id', '=', xml_rec.res_id)], limit = 1)


    return rec, is_new


class Demo(models.AbstractModel):
    _name = 'payroll.wage.history.demo'

    def _get_latest(self, model_name, domain):
        return self.env[model_name].search(domain, order='id desc', limit=1)

    @api.model
    def _init_demo_data(self):
        # dep_1 = self.env['hr.department'].create({'name': 'Department 1'})
        sales_dep, _ = create_with_xml_id(self, 'hr.department', {
            'name': 'Sales Department',
            'xml_id': 'sales_dep'
        })

        oliver, _ = create_with_xml_id(self, 'hr.employee', {
            'xml_id': 'oliver_emp',
            'name': 'Oliver',
            'job_title': 'Sales Officer',
            'department_id': sales_dep.id
        })
        jack, _ = create_with_xml_id(self, 'hr.employee', {
            'xml_id': 'jack_emp',
            'name': 'Jack',
            'job_title': 'Sales Manager',
            'department_id': sales_dep.id
        })
        sales_officer, _ = create_with_xml_id(self, 'hr.job', {
            'xml_id': 'sales_officer_job',
            'name': 'Sales Officer'
        })
        sales_manager, _ = create_with_xml_id(self, 'hr.job', {
            'xml_id': 'sales_manager_job',
            'name': 'Sales Manager'
        })
        # = self.env['hr.job'].create({'name': 'Job 1'})
        oliver_contract, _ = create_with_xml_id(self, 'hr.contract', {
            'xml_id': 'oliver_sales_officer_contract',
            'name': 'Sales Officer (Oliver)',
            'wage': 10,
            'job_id': sales_officer.id,
            'department_id': sales_dep.id,
            'employee_id': oliver.id,
        })
        jack_contract, is_new = create_with_xml_id(self, 'hr.contract', {
            'xml_id': 'jack_sales_manager_contract',
            'name': 'Sales Manager (Jack)',
            'wage': 20,
            'job_id': sales_manager.id,
            'department_id': sales_dep.id,
            'employee_id': jack.id
        })
        if is_new:
            jack_contract.write({'wage': 45.5})
            oliver_domain = [('contract_id', '=', oliver_contract.id)]
            pwh = self._get_latest('payroll.wage.history', oliver_domain)
            pwh.write({'effective_date': '2019-9-22'})
            oliver_contract.write({'wage': 15.5})
            pwh = self._get_latest('payroll.wage.history', oliver_domain)
            pwh.write({'effective_date': '2019-9-23'})
            oliver_contract.write({'wage': 25.5})
            pwh = self._get_latest('payroll.wage.history', oliver_domain)
            pwh.write({'effective_date': '2019-9-24'})
