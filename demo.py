import os
from bmail.llm_email_tools import send_email, check_inbox, read_email, archive_emails, reply_to_email
import time

def main():
    # All credentials will be taken from environment variables:
    # BMAIL_CREDENTIALS_PATH: Path to service account key file
    # BMAIL_TEST_EMAIL: Email used for testing
    # BMAIL_SENDER: Default sender email for the bot
    test_email = os.environ['BMAIL_TEST_EMAIL']
    sender = os.environ['BMAIL_SENDER']

    print("\n1. Sending test email...")
    result = send_email(
        to=test_email,
        cc="",
        bcc="",
        subject="TEST EMAIL",
        body="This is a test email from the demo script."
        cc="",
        bcc="",
        subject="TEST EMAIL",
        body="This is a test email from the demo script."
    )
    print(f"Send result: {result}")
    
    # Wait a moment for email delivery
    print("\n2. Waiting 5 seconds for email delivery...")
    time.sleep(5)
    
    print("\n3. Checking inbox for responses...")
    inbox_contents = check_inbox()
    print(f"Inbox contents:\n{inbox_contents}")
    
    print("\n4. Reading any messages...")
    # Split inbox contents into lines and extract email IDs
    messages = [line.split(":")[0].strip() for line in inbox_contents.split("\n") if line.strip()]
    for msg_id in messages:
        if msg_id:
            content = read_email(msg_id)
            print(f"\nMessage content:\n{content}")
    
    print("\n5. Archiving test emails...")
    for msg_id in messages:
        if msg_id:
            archived = archive_emails(msg_id)
            print(f"Archive result for {msg_id}: {archived}")

if __name__ == "__main__":
    main()
