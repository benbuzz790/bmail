import unittest
import os
from pathlib import Path
import shutil
from bmail.storage import save_email, read_email, move_email, list_emails, delete_email

class TestStorage(unittest.TestCase):
    """Test cases for storage.py functionality."""

    def setUp(self):
        """Create test folders and sample data before each test."""
        self.test_folders = ['inbox', 'sent', 'archive']
        self.sample_email = b'From: test@example.com\nSubject: Test\n\nTest content'
        self.test_email_id = 'test1.eml'
        for folder in self.test_folders:
            Path(folder).mkdir(exist_ok=True)

    def tearDown(self):
        """Clean up test folders and files after each test."""
        for folder in self.test_folders:
            if Path(folder).exists():
                shutil.rmtree(folder)

    def test_save_email(self):
        """Test saving email content to a folder."""
        result = save_email('inbox', self.test_email_id, self.sample_email)
        self.assertTrue(result.startswith('Success'))
        self.assertTrue(Path('inbox', self.test_email_id).exists())
        result = save_email('invalid', self.test_email_id, self.sample_email)
        self.assertTrue(result.startswith('Error'))
        result = save_email('inbox', 'test.txt', self.sample_email)
        self.assertTrue(result.startswith('Error'))

    def test_read_email(self):
        """Test reading email content from a folder."""
        save_email('inbox', self.test_email_id, self.sample_email)
        content = read_email('inbox', self.test_email_id)
        self.assertEqual(content, self.sample_email)
        result = read_email('inbox', 'nonexistent.eml')
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result.startswith('Error'))

    def test_move_email(self):
        """Test moving email between folders."""
        save_email('inbox', self.test_email_id, self.sample_email)
        result = move_email('inbox', 'archive', self.test_email_id)
        self.assertTrue(result.startswith('Success'))
        self.assertFalse(Path('inbox', self.test_email_id).exists())
        self.assertTrue(Path('archive', self.test_email_id).exists())
        result = move_email('inbox', 'archive', 'nonexistent.eml')
        self.assertTrue(result.startswith('Error'))

    def test_list_emails(self):
        """Test listing emails in a folder."""
        result = list_emails('inbox')
        self.assertEqual(result, 'No emails found in inbox')
        save_email('inbox', 'test1.eml', self.sample_email)
        save_email('inbox', 'test2.eml', self.sample_email)
        result = list_emails('inbox')
        self.assertIn('test1.eml', result)
        self.assertIn('test2.eml', result)
        result = list_emails('invalid')
        self.assertTrue(result.startswith('Error'))

    def test_delete_email(self):
        """Test deleting an email."""
        save_email('inbox', self.test_email_id, self.sample_email)
        result = delete_email('inbox', self.test_email_id)
        self.assertTrue(result.startswith('Success'))
        self.assertFalse(Path('inbox', self.test_email_id).exists())
        result = delete_email('inbox', 'nonexistent.eml')
        self.assertTrue(result.startswith('Error'))
        result = delete_email('invalid', self.test_email_id)
        self.assertTrue(result.startswith('Error'))