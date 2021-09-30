# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    advance_id = fields.Many2one('account.advance.payment', copy=False)
    # invoice fields
    advance_payment_ids = fields.One2many('account.advance.payment.apply', 'invoice_id', string='Advance Payments')
    amount_advance_available_customer = fields.Monetary(related='partner_id.customer_advance_available',
        currency_field='company_currency_id')
    amount_advance_available_invoice_customer  = fields.Monetary(compute='_compute_amount_advance_available_invoice_customer')
    amount_advance_available_supplier = fields.Monetary(related='partner_id.supplier_advance_available',
        currency_field='company_currency_id')
    amount_advance_available_invoice_supplier  = fields.Monetary(compute='_compute_amount_advance_available_invoice_supplier')
    invoice_in_foreign_currency = fields.Boolean(compute='_compute_invoice_in_foreign_currency')

    @api.depends('currency_id', 'company_currency_id')
    def _compute_invoice_in_foreign_currency(self):
        for invoice in self:
            if invoice.currency_id != invoice.company_currency_id:
                invoice.invoice_in_foreign_currency = True
            else:
                invoice.invoice_in_foreign_currency = False

    @api.depends('amount_advance_available_customer', 'currency_id', 'company_currency_id')
    def _compute_amount_advance_available_invoice_customer(self):
        today = fields.Date.today()   
        for invoice in self:
            company_currency = invoice.company_currency_id.with_context(date=today)
            amount = company_currency.compute(invoice.amount_advance_available_customer, invoice.currency_id)
            invoice.amount_advance_available_invoice_customer = amount
    
    @api.depends('amount_advance_available_supplier', 'currency_id', 'company_currency_id')
    def _compute_amount_advance_available_invoice_supplier(self):
        today = fields.Date.today()   
        for invoice in self:
            company_currency = invoice.company_currency_id.with_context(date=today)
            amount = company_currency.compute(invoice.amount_advance_available_supplier, invoice.currency_id)
            invoice.amount_advance_available_invoice_supplier = amount


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    advance_id = fields.Many2one('account.advance.payment', related='move_id.advance_id')
    payment_advance_id = fields.Many2one('account.advance.payment', string="Originator Payment", copy=False, help="Payment that created this entry")