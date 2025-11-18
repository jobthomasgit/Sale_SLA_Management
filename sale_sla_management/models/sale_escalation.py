from odoo import models, fields


class SaleEscalation(models.Model):
    _name = 'sale.escalation'
    _description = 'Sale Escalation'
    _rec_name = 'sale_order_id'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    escalation_reason = fields.Text(string='Escalation Reason', required=True)
    responsible_user_id = fields.Many2one('res.users', string='Responsible User', required=True,
                                          default=lambda self: self.env.user)


    def action_confirm_escalation(self):
        self.sale_order_id.is_escalated = True
        message = f"Order escalated by {self.responsible_user_id.name} for reason: {self.escalation_reason}"
        self.sale_order_id.message_post(body=message)

