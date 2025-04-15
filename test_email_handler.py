import unittest
import os
from bmail.email_handler import send_email, receive_email, archive_email, list_emails
from bmail.config import Config

class TestEmailHandler(unittest.TestCase):
    """Test cases for email_handler.py using real Gmail API integration."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.creds_path = Config.CREDENTIALS_PATH
        if not os.path.exists(cls.creds_path):
            raise unittest.SkipTest(f'{cls.creds_path} not found - skipping tests')
        cls.test_recipient = Config.TEST_EMAIL
        cls.test_subject = 'Test Email Subject'
        cls.test_body = 'This is a test email body.'

    def test_send_email(self):
        """Test sending an email."""
        result = send_email(self.creds_path, self.test_recipient, '', '', self.test_subject, self.test_body)
        self.assertTrue(result.startswith('Email sent successfully'))

    def test_receive_email(self):
        """Test receiving a specific email."""
        send_result = send_email(self.creds_path, self.test_recipient, '', '', self.test_subject, self.test_body)
        email_id = send_result.split('Message ID: ')[1]
        result = receive_email(self.creds_path, email_id)
        self.assertIsInstance(result, str)
        self.assertTrue(self.test_subject in result, 'Subject not found in email content')
        self.assertTrue(self.test_body in result, 'Body not found in email content')

    def test_archive_email(self):
        """Test archiving an email."""
        send_result = send_email(self.creds_path, self.test_recipient, '', '', self.test_subject, self.test_body)
        email_id = send_result.split('Message ID: ')[1]
        receive_email(self.creds_path, email_id)
        result = archive_email(self.creds_path, email_id)
        self.assertTrue(result.endswith('archived successfully'))

    def test_list_emails(self):
        """Test listing emails in inbox."""
        send_email(self.creds_path, self.test_recipient, '', '', self.test_subject, self.test_body)
        result = list_emails(self.creds_path)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, '')
        self.assertNotIn('error', result.lower())