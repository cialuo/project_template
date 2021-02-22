
{
    'name': 'Project Category',
    'version': '12.0.1.0.0',
    'category': 'Projects',
    'summary': 'manage and create categories to project.',
    'description': """ 
        By Using this odoo application you can configure category of project
        and assign category to the project.
                    """,
    'author': 'Malek Abushabab',
    'support':'malik@newsolutions.ps',
    'website': "https://github.com/MalekShabab/Project-Category",
    'license': 'AGPL-3',
    'images': ['static/description/main.png'],
    'depends': ['base','project'],
    'data': [
        'security/ir.model.access.csv',  
        'views/project_view.xml',
        'views/menu_item.xml',
        ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
