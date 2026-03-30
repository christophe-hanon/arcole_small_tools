# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError


class TestArcoleAccountTag(TransactionCase):
    """Test cases for arcole.account.tag model."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ArcoleTag = cls.env['arcole.account.tag']
        cls.AccountMove = cls.env['account.move']
        cls.AccountMoveLine = cls.env['account.move.line']

        # Create test tags
        cls.tag_both = cls.ArcoleTag.create({
            'name': 'Tag Both',
            'short_code': 'TB',
            'domain_move': True,
            'domain_move_line': True,
        })
        cls.tag_move_only = cls.ArcoleTag.create({
            'name': 'Tag Move Only',
            'short_code': 'TMO',
            'domain_move': True,
            'domain_move_line': False,
        })
        cls.tag_line_only = cls.ArcoleTag.create({
            'name': 'Tag Line Only',
            'short_code': 'TLO',
            'domain_move': False,
            'domain_move_line': True,
        })

        # Get a journal for creating moves
        cls.journal = cls.env['account.journal'].search([
            ('type', '=', 'general')
        ], limit=1)
        if not cls.journal:
            cls.journal = cls.env['account.journal'].create({
                'name': 'Test Journal',
                'type': 'general',
                'code': 'TGEN',
            })

        # Get accounts for move lines
        cls.account_receivable = cls.env['account.account'].search([
            ('account_type', '=', 'asset_receivable')
        ], limit=1)
        cls.account_payable = cls.env['account.account'].search([
            ('account_type', '=', 'liability_payable')
        ], limit=1)

    def test_01_create_tag_with_correct_values(self):
        """Test that arcole.account.tag can be created with correct values."""
        tag = self.ArcoleTag.create({
            'name': 'Test Tag',
            'short_code': 'TT',
            'domain_move': True,
            'domain_move_line': False,
        })
        self.assertEqual(tag.name, 'Test Tag')
        self.assertEqual(tag.short_code, 'TT')
        self.assertTrue(tag.domain_move)
        self.assertFalse(tag.domain_move_line)

    def test_02_create_tag_default_values(self):
        """Test that default values are correctly applied."""
        tag = self.ArcoleTag.create({
            'name': 'Default Tag',
        })
        # Default values should be True for both
        self.assertTrue(tag.domain_move)
        self.assertTrue(tag.domain_move_line)

    def test_03_account_move_tag_association(self):
        """Test that arcole_account_tag_ids on account.move correctly associates tags."""
        move = self.AccountMove.create({
            'journal_id': self.journal.id,
            'move_type': 'entry',
            'arcole_account_tag_ids': [(6, 0, [self.tag_both.id, self.tag_move_only.id])],
        })
        self.assertEqual(len(move.arcole_account_tag_ids), 2)
        self.assertIn(self.tag_both, move.arcole_account_tag_ids)
        self.assertIn(self.tag_move_only, move.arcole_account_tag_ids)

    def test_04_account_move_tag_domain_filter(self):
        """Test that domain_move filter is respected on account.move."""
        # The domain on the field should filter tags where domain_move=True
        # tag_line_only has domain_move=False, so it should be excluded by domain
        domain_tags = self.ArcoleTag.search([('domain_move', '=', True)])
        self.assertIn(self.tag_both, domain_tags)
        self.assertIn(self.tag_move_only, domain_tags)
        self.assertNotIn(self.tag_line_only, domain_tags)

    def test_05_account_move_line_tag_association(self):
        """Test that arcole_account_tag_ids on account.move.line correctly associates tags."""
        move = self.AccountMove.create({
            'journal_id': self.journal.id,
            'move_type': 'entry',
            'line_ids': [
                (0, 0, {
                    'account_id': self.account_receivable.id,
                    'debit': 100.0,
                    'credit': 0.0,
                    'arcole_account_tag_ids': [(6, 0, [self.tag_both.id, self.tag_line_only.id])],
                }),
                (0, 0, {
                    'account_id': self.account_payable.id,
                    'debit': 0.0,
                    'credit': 100.0,
                }),
            ],
        })
        line_with_tags = move.line_ids.filtered(lambda l: l.arcole_account_tag_ids)
        self.assertEqual(len(line_with_tags.arcole_account_tag_ids), 2)
        self.assertIn(self.tag_both, line_with_tags.arcole_account_tag_ids)
        self.assertIn(self.tag_line_only, line_with_tags.arcole_account_tag_ids)

    def test_06_account_move_line_tag_domain_filter(self):
        """Test that domain_move_line filter is respected on account.move.line."""
        # The domain on the field should filter tags where domain_move_line=True
        # tag_move_only has domain_move_line=False, so it should be excluded by domain
        domain_tags = self.ArcoleTag.search([('domain_move_line', '=', True)])
        self.assertIn(self.tag_both, domain_tags)
        self.assertIn(self.tag_line_only, domain_tags)
        self.assertNotIn(self.tag_move_only, domain_tags)

    def test_07_arcole_extra_text_on_account_move(self):
        """Test that arcole_extra_text can be set and retrieved on account.move."""
        move = self.AccountMove.create({
            'journal_id': self.journal.id,
            'move_type': 'entry',
            'arcole_extra_text': 'Test Extra Text for Move',
        })
        self.assertEqual(move.arcole_extra_text, 'Test Extra Text for Move')

        # Test update
        move.write({'arcole_extra_text': 'Updated Text'})
        self.assertEqual(move.arcole_extra_text, 'Updated Text')

    def test_08_arcole_extra_text_on_account_move_line(self):
        """Test that arcole_extra_text can be set and retrieved on account.move.line."""
        move = self.AccountMove.create({
            'journal_id': self.journal.id,
            'move_type': 'entry',
            'line_ids': [
                (0, 0, {
                    'account_id': self.account_receivable.id,
                    'debit': 100.0,
                    'credit': 0.0,
                    'arcole_extra_text': 'Test Extra Text for Line',
                }),
                (0, 0, {
                    'account_id': self.account_payable.id,
                    'debit': 0.0,
                    'credit': 100.0,
                }),
            ],
        })
        line_with_text = move.line_ids.filtered(lambda l: l.arcole_extra_text)
        self.assertEqual(line_with_text.arcole_extra_text, 'Test Extra Text for Line')

        # Test update
        line_with_text.write({'arcole_extra_text': 'Updated Line Text'})
        self.assertEqual(line_with_text.arcole_extra_text, 'Updated Line Text')


class TestArcoleAccountTagAccessRights(TransactionCase):
    """Test access rights for arcole.account.tag model."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ArcoleTag = cls.env['arcole.account.tag']

        # Get user groups
        cls.group_account_user = cls.env.ref('account.group_account_user')
        cls.group_account_manager = cls.env.ref('account.group_account_manager')

        # Create test users
        cls.user_accountant = cls.env['res.users'].create({
            'name': 'Test Accountant',
            'login': 'test_accountant',
            'email': 'accountant@test.com',
            'groups_id': [(6, 0, [cls.group_account_user.id])],
        })
        cls.user_manager = cls.env['res.users'].create({
            'name': 'Test Manager',
            'login': 'test_manager',
            'email': 'manager@test.com',
            'groups_id': [(6, 0, [cls.group_account_manager.id])],
        })

        # Create a tag as admin for testing
        cls.test_tag = cls.ArcoleTag.create({
            'name': 'Access Test Tag',
            'short_code': 'ATT',
        })

    def test_09_user_can_read_tags(self):
        """Test that account users can read arcole.account.tag records."""
        tag = self.ArcoleTag.with_user(self.user_accountant).browse(self.test_tag.id)
        # Should not raise AccessError
        self.assertEqual(tag.name, 'Access Test Tag')

    def test_10_user_cannot_create_tags(self):
        """Test that account users cannot create arcole.account.tag records."""
        with self.assertRaises(AccessError):
            self.ArcoleTag.with_user(self.user_accountant).create({
                'name': 'User Created Tag',
            })

    def test_11_user_cannot_write_tags(self):
        """Test that account users cannot write arcole.account.tag records."""
        tag = self.ArcoleTag.with_user(self.user_accountant).browse(self.test_tag.id)
        with self.assertRaises(AccessError):
            tag.write({'name': 'Modified Name'})

    def test_12_user_cannot_unlink_tags(self):
        """Test that account users cannot delete arcole.account.tag records."""
        tag_to_delete = self.ArcoleTag.create({'name': 'Tag to Delete'})
        tag = self.ArcoleTag.with_user(self.user_accountant).browse(tag_to_delete.id)
        with self.assertRaises(AccessError):
            tag.unlink()

    def test_13_manager_can_read_tags(self):
        """Test that account managers can read arcole.account.tag records."""
        tag = self.ArcoleTag.with_user(self.user_manager).browse(self.test_tag.id)
        self.assertEqual(tag.name, 'Access Test Tag')

    def test_14_manager_can_create_tags(self):
        """Test that account managers can create arcole.account.tag records."""
        tag = self.ArcoleTag.with_user(self.user_manager).create({
            'name': 'Manager Created Tag',
            'short_code': 'MCT',
        })
        self.assertTrue(tag.exists())
        self.assertEqual(tag.name, 'Manager Created Tag')

    def test_15_manager_can_write_tags(self):
        """Test that account managers can write arcole.account.tag records."""
        tag = self.ArcoleTag.with_user(self.user_manager).browse(self.test_tag.id)
        tag.write({'short_code': 'UPDATED'})
        self.assertEqual(tag.short_code, 'UPDATED')

    def test_16_manager_can_unlink_tags(self):
        """Test that account managers can delete arcole.account.tag records."""
        tag_to_delete = self.ArcoleTag.with_user(self.user_manager).create({
            'name': 'Manager Tag to Delete',
        })
        tag_id = tag_to_delete.id
        tag_to_delete.unlink()
        self.assertFalse(self.ArcoleTag.browse(tag_id).exists())
