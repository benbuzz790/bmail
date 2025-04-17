import os
from typing import Union
from email import message_from_string
from email.message import EmailMessage
from email.mime.text import MIMEText
import base64
from bmail.auth import get_gmail_service
from bmail import gmail_client

def _get_service(creds_path: str, use_sender: bool=True) -> Union[str, object]:
    """Get Gmail service using credentials and delegated email from environment.
    
    Args:
        creds_path: Path to credentials file
        use_sender: If True, use BMAIL_SENDER, otherwise use BMAIL_TEST_EMAIL
    """
    try:
        env_var = 'BMAIL_SENDER' if use_sender else 'BMAIL_TEST_EMAIL'
        delegated_email = os.environ[env_var]
        return get_gmail_service(creds_path, delegated_email)
    except KeyError:
        return f'Error: {env_var} environment variable not set'

def send_email(creds_path: str, to_addr: str, cc: str, bcc: str, subject: str, body: str, thread_id: str=None, in_reply_to: str=None, references: str=None) -> str:
    """Send an email using Gmail API.

    Args:
        creds_path (str): Path to Gmail API credentials file
        to_addr (str): Recipient email address
        cc (str): CC recipients (comma-separated)
        bcc (str): BCC recipients (comma-separated)
        subject (str): Email subject
        body (str): Email body text
        thread_id (str, optional): Gmail thread ID for replies
        in_reply_to (str, optional): Message-ID being replied to
        references (str, optional): References header for threading

    Returns:
        str: Success message or error description
    """
    service = _get_service(creds_path)
    if isinstance(service, str):
        return f'Authentication error: {service}'
    return gmail_client.send_gmail(service, to_addr, cc, bcc, subject, body, thread_id, in_reply_to, references)

def receive_email(creds_path: str, email_id: str) -> str:
    """Receive a specific email.

    Args:
        creds_path (str): Path to Gmail API credentials file
        email_id (str): Gmail message ID to fetch

    Returns:
        str: Formatted email content or error description
    """
    service = _get_service(creds_path)
    if isinstance(service, str):
        return f'Authentication error: {service}'
    result = gmail_client.get_email(service, email_id)
    if isinstance(result, str):
        return result
    if not isinstance(result, tuple) or len(result) != 2:
        return 'Error: Unexpected response format from gmail_client'
    raw_content, metadata = result
    try:
        from email import message_from_bytes
        email_msg = message_from_bytes(raw_content)
        formatted_content = []
        formatted_content.append(f"From: {email_msg['from']}")
        formatted_content.append(f"Subject: {email_msg['subject']}")
        formatted_content.append(f"To: {email_msg['to']}")
        if metadata.get('message_id'):
            formatted_content.append(f"Message-ID: {metadata['message_id']}")
        if metadata.get('thread_id'):
            formatted_content.append(f"Thread-ID: {metadata['thread_id']}")
        formatted_content.append('\nBody:')
        if email_msg.is_multipart():
            for part in email_msg.walk():
                if part.get_content_type() == 'text/plain':
                    formatted_content.append(part.get_payload(decode=True).decode('utf-8'))
        else:
            payload = email_msg.get_payload(decode=True)
            if payload:
                formatted_content.append(payload.decode('utf-8'))
            else:
                formatted_content.append(email_msg.get_payload())
        return '\n'.join(formatted_content)
    except Exception as e:
        return f'Error parsing email content: {str(e)}'

def archive_email(creds_path: str, email_id: str, use_sender: bool=True) -> str:
    """Archive an email.

    Args:
        creds_path (str): Path to Gmail API credentials file
        email_id (str): ID of email to archive
        use_sender (bool): If True, use BMAIL_SENDER account, else use TEST_EMAIL

    Returns:
        str: Success message or error description
    """
    gmail_id = email_id.replace('.eml', '') if email_id.endswith('.eml') else email_id
    service = _get_service(creds_path, use_sender)
    if isinstance(service, str):
        return f'Authentication error: {service}'
    return gmail_client.archive_email(service, gmail_id)

def list_emails(creds_path: str, query: str=None, use_sender: bool=True) -> str:
    """List emails in the inbox.

    Args:
        creds_path (str): Path to Gmail API credentials file
        query (str, optional): Gmail search query to filter results
        use_sender (bool): If True, use BMAIL_SENDER account, else use TEST_EMAIL

    Returns:
        str: Newline-separated list of "sender: subject" or error message
    """
    service = _get_service(creds_path, use_sender)
    if isinstance(service, str):
        return f'Authentication error: {service}'
    return gmail_client.list_emails(service, query=query)
    return gmail_client.list_emails(service, query=query)