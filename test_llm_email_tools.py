import unittest
import os
import time
from bmail import llm_email_tools

class TestLLMEmailTools(unittest.TestCase):
    """Test LLM email tools interface."""

    @classmethod
    def setUpClass(cls):
        """Set up test parameters."""
        cls.cred_filepath = os.environ['BMAIL_CREDENTIALS_PATH']
        if not os.path.exists(cls.cred_filepath):
            raise unittest.SkipTest(f'{cls.cred_filepath} not found - skipping tests')
        cls.test_email = os.environ['BMAIL_TEST_EMAIL']
        cls.sender = os.environ['BMAIL_SENDER']
        cls.test_subject = 'TEST EMAIL'
        cls.test_body = 'This is a test email.'
        cls.email_id = None

    def test_1_send_email(self):
        """Test sending an email."""
        result = llm_email_tools.send_email(to=self.test_email, cc='', bcc='', subject=self.test_subject, body=self.test_body, cred_filepath=self.cred_filepath)
        self.assertTrue('successfully' in result.lower())
        if 'Message ID: ' in result:
            self.__class__.email_id = result.split('Message ID: ')[1]
        time.sleep(5)

    def test_2_check_inbox(self):
        """Test inbox listing using sender account."""
        # First check that inbox is being checked from sender account
        result = llm_email_tools.check_inbox(cred_filepath=self.cred_filepath)
        self.assertIsInstance(result, str)
        
        # Send test email to sender account
        send_result = llm_email_tools.send_email(
            to=self.sender,  # Send to sender account
            cc='',
            bcc='',
            subject=self.test_subject,
            body=self.test_body,
            cred_filepath=self.cred_filepath
        )
        self.assertTrue('successfully' in send_result.lower())
        time.sleep(5)  # Wait for email to arrive
        
        # Check sender's inbox for the test email
        result = llm_email_tools.check_inbox(
            query=f'subject:"{self.test_subject}"',
            cred_filepath=self.cred_filepath
        )
        self.assertIsInstance(result, str)
        self.assertTrue(self.test_subject in result, 'Test subject not found in sender inbox')

    def test_3_read_and_reply(self):
        """Test reading and replying to the test email."""
        self.assertIsNotNone(self.email_id, 'No test email ID available')
        result = llm_email_tools.read_email(email_id=self.email_id, cred_filepath=self.cred_filepath)
        self.assertIsInstance(result, str)
        self.assertTrue(self.test_subject in result)
        self.assertTrue(self.test_body in result)
        reply_text = 'This is an automated test reply.'
        result = llm_email_tools.reply_to_email(email_id=self.email_id, body=reply_text, sender=self.sender, cred_filepath=self.cred_filepath)
        self.assertTrue('successfully' in result.lower())

    def test_4_archive(self):
        """Test archiving the test email and verify it's removed from inbox."""
        # Create unique subject for this test
        test_subject = f"Archive Test {time.time()}"
        
        # Send a test email to the sender account first
        send_result = llm_email_tools.send_email(
            to=self.sender,
            cc='',
            bcc='',
            subject=test_subject,
            body="This is a test email for archiving",
            cred_filepath=self.cred_filepath
        )
        self.assertTrue('successfully' in send_result.lower())
        email_id = send_result.split('Message ID: ')[1]
        time.sleep(5)  # Wait for email to arrive
        
        # Verify the test email exists in sender's inbox
        pre_archive = llm_email_tools.check_inbox(
            query=f'subject:"{test_subject}"',
            cred_filepath=self.cred_filepath
        )
        self.assertTrue(test_subject in pre_archive, 'Test email not found in sender inbox before archiving')
        
        # Archive the email
        result = llm_email_tools.archive_emails(email_id, self.cred_filepath)
        self.assertTrue('successfully' in result.lower(), f"Archive failed with result: {result}")
        
        # Allow time for Gmail API to process the archive operation
        time.sleep(5)
        
        # Verify email no longer appears in sender's inbox
        post_archive = llm_email_tools.check_inbox(
            query=f'subject:"{test_subject}"',
            cred_filepath=self.cred_filepath
        )
        self.assertNotIn(test_subject, post_archive, 'Test email still found in sender inbox after archiving')
if __name__ == '__main__':
    unittest.main()
