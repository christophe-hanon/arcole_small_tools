# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    arcole_account_tag_ids = fields.Many2many(
        comodel_name='arcole.account.tag',
        relation='account_move_arcole_tag_rel',
        column1='move_id',
        column2='tag_id',
        string='Extra Tags',
        domain="[('domain_move', '=', True)]",
    )
    #hint-optional-show
    arcole_extra_text = fields.Char(string='Extra Text')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    arcole_account_tag_ids = fields.Many2many(
        comodel_name='arcole.account.tag',
        relation='account_move_line_arcole_tag_rel',
        column1='move_line_id',
        column2='tag_id',
        string='Extra Tags',
        domain="[('domain_move_line', '=', True)]",
    )
    #hint-optional-show
    arcole_extra_text = fields.Char(string='Extra Text')
