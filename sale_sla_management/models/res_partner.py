from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_tier = fields.Selection(
        [
            ('bronze', 'Bronze'),
            ('silver', 'Silver'),
            ('gold', 'Gold'),
        ], string='Customer Tier'
    )
    default_sla = fields.Selection(
        [
            ('standard', 'Standard'),
            ('priority', 'Priority'),
            ('urgent', 'Urgent'),
        ], string='Default SLA'
    )
