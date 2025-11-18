from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sla_level = fields.Selection(
        [
            ('standard', 'Standard'),
            ('priority', 'Priority'),
            ('urgent', 'Urgent'),
        ], string='SLA Level', compute='_compute_sla_level', store=True, tracking=True
    )
    is_escalated = fields.Boolean(string='Is Escalated', default=False)
    is_revised_order = fields.Boolean(string='Is Revised Order', default=False, copy=False)
    revision_number = fields.Integer(string='Revision Number', default=0, copy=False)
    original_name = fields.Char(string='Original Name', copy=False)
    original_sale_id = fields.Many2one('sale.order', string='Original Sale Order', copy=False)
    escalation_count = fields.Integer(string='Escalation Count', compute='_compute_escalation_count')

    @api.depends('partner_id', 'amount_total')
    def _compute_sla_level(self):
        for order in self:
            customer_tier = order.partner_id.customer_tier
            if customer_tier == 'gold' or (customer_tier == 'silver' and order.amount_total > 10000):
                order.sla_level = 'urgent'
            elif customer_tier == 'silver':
                order.sla_level = 'priority'
            else:
                order.sla_level = order.partner_id.default_sla or 'standard'

    def _compute_escalation_count(self):
        for order in self:
            count = self.env['sale.escalation'].search_count([('sale_order_id', '=', order.id)])
            order.escalation_count = count

    def action_open_escalation_wizard(self):
        return {
            'name': 'Sale Escalation',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.escalation',
            'view_mode': 'form',
            'view_id': self.env.ref('sale_sla_management.sale_escalation_form').id,
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id,
            },
        }

    def action_open_escalated_history(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Escalation History",
            "res_model": "sale.escalation",
            "view_mode": "list,form",
            "context": {
                "create": False,
                "edit": False,
                "delete": False,
            },
            "domain": [("sale_order_id", "=", self.id)],
        }

    def revise_sale_order(self):
        for order in self:
            vals = {
                "name": order.name,
                "is_revised_order": True,
                "revision_number": order.revision_number,
                "original_sale_id": order.id,
                "is_escalated": order.is_escalated,
                "state": "cancel",
            }
            order.copy(default=vals)
            order.revision_number += 1
            new_name = f"{order.original_name}-Rev{order.revision_number}" if order.original_name else f"{order.name}-Rev{order.revision_number}"
            order.write({
                'name': new_name,
                'is_escalated': False,
                'state': 'draft',
            })

    def action_open_revision_history(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Revised History",
            "res_model": "sale.order",
            "view_mode": "list,form",
            "context": {
                "create": False,
                "edit": False,
                "delete": False,
            },
            "domain": [("original_sale_id", "=", self.id)],
        }

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record.original_name = record.name
        return records
