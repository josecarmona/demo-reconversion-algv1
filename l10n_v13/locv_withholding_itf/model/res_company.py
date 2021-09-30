# coding: utf-8
###########################################################################

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'account.journal'

    calculate_wh_itf = fields.Boolean(
        'Retención automática de IGTF',
        help='Cuando sea Verdadero, la Retención de la IGTF del Proveedor se comprobará y'
        'se validará automáticamente', default=True)
    wh_porcentage = fields.Float(
        'Porcentaje IGTF', help="El porcentaje a aplicar para retener", default=2.0)

    account_wh_itf_id = fields.Many2one('account.account', string="Cuenta IGTF", help="Esta cuenta se utilizará en lugar de la predeterminada"
                                        "para generar el asiento del IGTF")

    @api.onchange('calculate_wh_itf')
    def _onchange_check_itf(self):

        if not self.calculate_wh_itf:
            self.write({'wh_porcentage': 0.0,
                        'account_wh_itf_id': False})
        else:
            self.write({'wh_porcentage': 2.0})

        return


