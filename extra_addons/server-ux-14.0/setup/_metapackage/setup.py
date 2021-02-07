import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-server-ux",
    description="Meta package for oca-server-ux Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-base_technical_features',
        'odoo14-addon-base_tier_validation',
        'odoo14-addon-base_tier_validation_formula',
        'odoo14-addon-base_tier_validation_forward',
        'odoo14-addon-date_range',
        'odoo14-addon-mass_editing',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
