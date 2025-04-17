import os
from typing import Optional
from bmail import email_handler

def send_email(to: str, cc: str, bcc: str, subject: str, body: str, cred_filepath: Optional[str]=None) -> str:
    """Send an email using Gmail API.
    
    Args:
        to: Recipient email address
        cc: Comma-separated CC addresses (can be empty)
        bcc: Comma-separated BCC addresses (can be empty)
        subject: Email subject line
        body: Email body text
        cred_filepath: Path to credentials.json file (optional - uses env vars by default)
        
    Returns:
        str: Success/error message
    
    Example:
        >>> send_email("credentials.json", "user@example.com", "", "", "Hello", "Test message")
        "Email sent successfully"
    """
    creds = cred_filepath or os.environ['BMAIL_CREDENTIALS_PATH']
    return email_handler.send_email(creds, to, cc, bcc, subject, body)

def reply_to_email(email_id: str, body: str, sender: str, cred_filepath: Optional[str]=None) -> str:
    """Reply to a specific email using Gmail API.

    Args:
        email_id: Unique identifier of the email to reply to
        body: Reply message body
        sender: Email address to send from (typically BMAIL_SENDER)
        cred_filepath: Path to credentials.json file (optional - uses env vars by default)

    Returns:
        str: Success/error message

    Example:
        >>> reply_to_email("12345", "Thanks for your email", "bot@example.com")
        "Reply sent successfully"
    """
    creds = cred_filepath or os.environ['BMAIL_CREDENTIALS_PATH']
    original = email_handler.receive_email(creds, email_id)
    if original.startswith('Error'):
        return original
    lines = original.split('\n')
    from_line = next((l for l in lines if l.startswith('From: ')), '')
    subject_line = next((l for l in lines if l.startswith('Subject: ')), '')
    message_id_line = next((l for l in lines if l.startswith('Message-ID: ')), '')
    thread_id_line = next((l for l in lines if l.startswith('Thread-ID: ')), '')
    if not from_line or not subject_line:
        return 'Error: Could not parse original email headers'
    original_sender = from_line.replace('From: ', '').strip()
    original_subject = subject_line.replace('Subject: ', '').strip()
    reply_subject = original_subject if original_subject.startswith('Re:') else f'Re: {original_subject}'
    message_id = message_id_line.replace('Message-ID: ', '').strip() if message_id_line else None
    thread_id = thread_id_line.replace('Thread-ID: ', '').strip() if thread_id_line else None
    return email_handler.send_email(creds, original_sender, '', '', reply_subject, body, thread_id=thread_id, in_reply_to=message_id, references=message_id)

def check_inbox(query: str=None, cred_filepath: Optional[str]=None) -> str:
    """List inbox contents using Gmail API.

    Args:
        query: Optional Gmail search query (e.g. 'subject:"TEST EMAIL"')
        cred_filepath: Path to credentials.json file (optional - uses env vars by default)

    Returns:
        str: Newline-separated list of "sender: subject"

    Example:
        >>> check_inbox("credentials.json")
        "user1@example.com: Hello
user2@example.com: Meeting"
        >>> check_inbox("credentials.json", query='subject:"TEST EMAIL"')
        "test@example.com: TEST EMAIL"
    """
    creds = cred_filepath or os.environ['BMAIL_CREDENTIALS_PATH']
    return email_handler.list_emails(creds, query=query)

def read_email(email_id: str, cred_filepath: Optional[str]=None) -> str:
    """Retrieve content of a specific email using Gmail API.
    
    Args:
        email_id: Unique identifier of the email to read
        cred_filepath: Path to credentials.json file (optional - uses env vars by default)

    Returns:
        str: Formatted email content
    
    Example:
        >>> read_email("credentials.json", "12345")
        "From: user@example.com
        Subject: Hello
        Body: Test message"
    """
    creds = cred_filepath or os.environ['BMAIL_CREDENTIALS_PATH']
    return email_handler.receive_email(creds, email_id)

def archive_emails(email_id: str, cred_filepath: Optional[str]=None) -> str:
    """Archive a specific email using Gmail API.
    
    Args:
        email_id: Unique identifier of the email to archive
        cred_filepath: Path to credentials.json file (optional - uses env vars by default)

    Returns:
        str: Success/error message
    
    Example:
        >>> archive_emails("credentials.json", "12345")
        "Email archived successfully"
    """
    creds = cred_filepath or os.environ['BMAIL_CREDENTIALS_PATH']
    return email_handler.archive_email(creds, email_id)