import unittest
import os
from auth_service import get_gmail_service, verify_service_account_setup


class TestServiceAuth(unittest.TestCase):
    """Test cases for service account authentication."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.service_account_path = 'service-credentials.json'
        if not os.path.exists(cls.service_account_path):
            raise unittest.SkipTest(
                'service-credentials.json not found - skipping service account tests'
                )

    def test_service_account_verification(self):
        """Test service account configuration verification."""
        result = verify_service_account_setup(self.service_account_path)
        self.assertIsInstance(result, str)
        self.assertNotIn('Error:', result)
        self.assertIn('successfully configured', result)

    def test_get_service(self):
        """Test getting Gmail service with service account."""
        service = get_gmail_service(self.service_account_path)
        self.assertNotIsInstance(service, str)
        try:
            profile = service.users().getProfile(userId='me').execute()
            self.assertIn('@', profile['emailAddress'])
        except Exception as e:
            self.fail(f'Failed to use Gmail API with service account: {str(e)}'
                )

    def test_missing_credentials(self):
        """Test handling of missing service account file."""
        service = get_gmail_service('nonexistent.json')
        self.assertIsInstance(service, str)
        self.assertIn('Error', service)
