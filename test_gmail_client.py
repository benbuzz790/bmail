import unittest
import os
from googleapiclient.discovery import Resource, build
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from bmail import gmail_client
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.send']

def get_test_service() -> Resource:
    """Get Gmail service with proper scopes for testing."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

class TestGmailClient(unittest.TestCase):
    """Integration tests for Gmail client using real Gmail API."""

    @classmethod
    def setUpClass(cls):
        """Set up Gmail service for all tests."""
        cls.service = get_test_service()
        cls.test_email = 'benbuzz790@gmail.com'
        cls.test_subject = 'TEST EMAIL'
        cls.test_body = 'This is a test email from the Gmail client integration tests.'

    def test_1_send_gmail(self):
        """Test sending an email."""
        print('\nSending test email...')
        result = gmail_client.send_gmail(self.service, self.test_email, '', '', self.test_subject, self.test_body)
        print(f'Send result: {result}')
        self.assertTrue('successfully' in result.lower())
        print('Waiting for email to propagate...')
        time.sleep(5)

    def test_2_list_emails(self):
        """Test listing emails."""
        print('\nTesting basic email listing...')
        result = gmail_client.list_emails(self.service)
        self.assertIsInstance(result, str)
        print('\nBasic email list result:')
        print(result)
        print('\nTesting specific email search...')
        search_query = f'subject:"{self.test_subject}"'
        print(f'Search query: {search_query}')
        result = gmail_client.list_emails(self.service, query=search_query)
        self.assertIsInstance(result, str)
        print('\nSearch result:')
        print(result)
        self.assertTrue(self.test_subject in result, f"Test subject '{self.test_subject}' not found in result")
        self.assertTrue(self.test_email in result)

    def test_3_get_email(self):
        """Test retrieving a specific email."""
        print('\nSearching for test email...')
        messages = self.service.users().messages().list(userId='me', q=f'subject:{self.test_subject}').execute().get('messages', [])
        print(f'Found {len(messages)} matching messages')
        self.assertTrue(len(messages) > 0)
        email_id = messages[0]['id']
        print(f'Using email ID: {email_id}')
        result = gmail_client.get_email(self.service, email_id)
        self.assertIsInstance(result, bytes)
        self.assertTrue(self.test_subject.encode() in result)

    def test_4_archive_email(self):
        """Test archiving an email."""
        print('\nFinding email to archive...')
        messages = self.service.users().messages().list(userId='me', q=f'subject:{self.test_subject}').execute().get('messages', [])
        print(f'Found {len(messages)} matching messages')
        self.assertTrue(len(messages) > 0)
        email_id = messages[0]['id']
        print(f'Archiving email ID: {email_id}')
        result = gmail_client.archive_email(self.service, email_id)
        self.assertTrue('archived successfully' in result.lower())
if __name__ == '__main__':
    unittest.main()