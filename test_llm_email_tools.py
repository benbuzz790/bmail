import unittest
import os
import time
from bmail import llm_email_tools
from bmail.config import Config

class TestLLMEmailTools(unittest.TestCase):
    """Test LLM email tools interface."""

    @classmethod
    def setUpClass(cls):
        """Set up test parameters."""
        cls.cred_filepath = Config.CREDENTIALS_PATH
        if not os.path.exists(cls.cred_filepath):
            raise unittest.SkipTest(f'{cls.cred_filepath} not found - skipping tests')
        cls.test_email = Config.TEST_EMAIL
        cls.test_subject = 'TEST EMAIL'
        cls.test_body = 'This is a test email.'
        cls.email_id = None

    def test_1_send_email(self):
        """Test sending an email."""
        result = llm_email_tools.send_email(self.cred_filepath, self.test_email, '', '', self.test_subject, self.test_body)
        self.assertTrue('successfully' in result.lower())
        if 'Message ID: ' in result:
            self.__class__.email_id = result.split('Message ID: ')[1]
        time.sleep(5)

    def test_2_check_inbox(self):
        """Test inbox listing."""
        result = llm_email_tools.check_inbox(self.cred_filepath)
        self.assertIsInstance(result, str)
        result = llm_email_tools.check_inbox(self.cred_filepath, query=f'subject:"{self.test_subject}"')
        self.assertIsInstance(result, str)
        self.assertTrue(self.test_subject in result)
        self.assertTrue(self.test_subject in result, 'Test subject not found in search results')

    def test_3_read_and_reply(self):
        """Test reading and replying to the test email."""
        self.assertIsNotNone(self.email_id, 'No test email ID available')
        result = llm_email_tools.read_email(self.cred_filepath, self.email_id)
        self.assertIsInstance(result, str)
        self.assertTrue(self.test_subject in result)
        self.assertTrue(self.test_body in result)
        reply_text = 'This is an automated test reply.'
        result = llm_email_tools.reply_to_email(self.cred_filepath, self.email_id, reply_text)
        self.assertTrue('successfully' in result.lower())

    def test_4_archive(self):
        """Test archiving the test email."""
        self.assertIsNotNone(self.email_id, 'No test email ID available')
        result = llm_email_tools.archive_emails(self.cred_filepath, self.email_id)
        self.assertTrue('successfully' in result.lower())
if __name__ == '__main__':
    unittest.main()
