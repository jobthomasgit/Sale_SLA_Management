{
    'name': 'Sales SLA Management',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Sales SLA Management',
    'description': 'Module to manage Service Level Agreements (SLA) for sales orders.',
    'author': 'Thomas Job',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/sale_escalation_views.xml',
    ],
    "auto_install": False,
    "application": False,
}
