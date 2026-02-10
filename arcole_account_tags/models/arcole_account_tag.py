# -*- coding: utf-8 -*-

from odoo import models, fields


class ArcoleAccountTag(models.Model):
    _name = 'arcole.account.tag'
    _description = 'Arcole Account Tag'

    name = fields.Char(string='Name', required=True)
    short_code = fields.Char(string='Short Code')
    domain_move = fields.Boolean(
        string='Applicable to Moves',
        default=True,
        help='If checked, this tag can be used on account.move records.',
    )
    domain_move_line = fields.Boolean(
        string='Applicable to Move Lines',
        default=True,
        help='If checked, this tag can be used on account.move.line records.',
    )
