# -*- coding: utf-8 -*-
{
    'name': 'Arcole Account Tags',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Add custom tags to account moves and move lines',
    'description': """
        This module adds a tagging system for account.move and account.move.line.
        Tags can be configured to apply to moves, move lines, or both.
        This part of the ADINS Arcole Small Tools project
    """,
    'author': 'C Hanon ADINS',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/arcole_account_tag_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
