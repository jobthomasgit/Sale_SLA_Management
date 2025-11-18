from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sla_level = fields.Selection(
        [
            ('standard', 'Standard'),
            ('priority', 'Priority'),
            ('urgent', 'Urgent'),
        ], string='SLA Level', compute='_compute_sla_level', store=True
    )
    is_escalated = fields.Boolean(string='Is Escalated', default=False)

    @api.depends('partner_id', 'amount_total', 'partner_id.customer_tier', 'partner_id.default_sla')
    def _compute_sla_level(self):
        for order in self:
            customer_tier = order.partner_id.customer_tier
            if customer_tier == 'gold' or (customer_tier == 'silver' and order.amount_total > 10000):
                order.sla_level = 'urgent'
            elif customer_tier == 'silver':
                order.sla_level = 'priority'
            else:
                order.sla_level = order.partner_id.default_sla or 'standard'

    def action_open_escalation_wizard(self):
        return {
            'name': 'Sale Escalation',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.escalation.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sale_sla_management.sale_escalation_wizard').id,
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id,
            },
        }