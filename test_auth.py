import unittest
import os
from bmail.auth import get_gmail_service
from googleapiclient.discovery import Resource

class TestAuth(unittest.TestCase):
    """Test cases for Gmail service account authentication."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.credentials_path = os.environ['BMAIL_CREDENTIALS_PATH']
        cls.test_email = os.environ['BMAIL_TEST_EMAIL']
        if not os.path.exists(cls.credentials_path):
            raise unittest.SkipTest(f'{cls.credentials_path} not found - skipping service account tests')

    def test_get_service(self):
        """Test getting Gmail service with service account."""
        service = get_gmail_service(self.credentials_path, self.test_email)
        self.assertNotIsInstance(service, str)
        try:
            profile = service.users().getProfile(userId='me').execute()
            self.assertIn('@', profile['emailAddress'])
            self.assertEqual(profile['emailAddress'], self.test_email)
        except Exception as e:
            self.fail(f'Failed to use Gmail API with service account: {str(e)}')

    def test_missing_credentials(self):
        """Test handling of missing service account file."""
        service = get_gmail_service('nonexistent.json', self.test_email)
        self.assertIsInstance(service, str)
        self.assertIn('Error: Credentials file not found', service)
