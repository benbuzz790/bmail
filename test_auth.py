import unittest
import os
from auth import get_gmail_service
from googleapiclient.discovery import Resource

class TestAuth(unittest.TestCase):
    """Test cases for Gmail authentication functionality."""

    def setUp(self):
        """Set up test environment."""
        self.valid_credentials_path = "credentials.json"
        self.invalid_credentials_path = "nonexistent.json"
        # Clean up any existing token
        if os.path.exists("token.pickle"):
            os.remove("token.pickle")

    def test_missing_credentials_file(self):
        """Test error handling when credentials file is missing."""
        result = get_gmail_service(self.invalid_credentials_path)
        self.assertIsInstance(result, str)
        self.assertTrue("Error: Credentials file not found" in result)

    def test_successful_authentication(self):
        """Test successful Gmail API authentication with valid credentials."""
        # Skip if no credentials.json present
        if not os.path.exists(self.valid_credentials_path):
            self.skipTest("credentials.json not found - skipping live API test")
        
        service = get_gmail_service(self.valid_credentials_path)
        self.assertIsInstance(service, Resource)

if __name__ == '__main__':
    unittest.main()
