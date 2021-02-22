from odoo import models, fields ,api

class project_category(models.Model):
    _name = 'project.category'
    _description = 'Project Category'
    name = fields.Char('Name',required=True)
    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)

    
    



class project(models.Model):
    _inherit = 'project.project'
    category_id = fields.Many2one('project.category', string='Category',store=True)

class task(models.Model):
    _inherit = 'project.task'

    @api.depends('project_id.category_id')
    def _compute_project_category(self):
        for task in self:
            task.project_category = task.project_id.category_id



    def _search_project_category(self, operator, value):
        return [('project_id.category_id', operator, value)]

    #  Enable write operations on a computed field
    def _inverse_project_category(self):
        for task in self:
            task.project_id.category_id = task.project_category
    
    project_category = fields.Many2one('project.category', string='Project Category' , inverse='_inverse_project_category',compute='_compute_project_category', search='_search_project_category', store=True)


    

    