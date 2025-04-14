import os
from typing import Union
from email import message_from_string
from email.message import EmailMessage
from email.mime.text import MIMEText
import base64
from bmail.auth import get_gmail_service
from bmail import gmail_client

def send_email(creds_path: str, to_addr: str, cc: str, bcc: str, subject: str, body: str) -> str:
    """Send an email using Gmail API.

    Args:
        creds_path (str): Path to Gmail API credentials file
        to_addr (str): Recipient email address
        cc (str): CC recipients (comma-separated)
        bcc (str): BCC recipients (comma-separated)
        subject (str): Email subject
        body (str): Email body text

    Returns:
        str: Success message or error description
    """
    service = get_gmail_service(creds_path)
    if isinstance(service, str):
        return f'Authentication error: {service}'
    return gmail_client.send_gmail(service, to_addr, cc, bcc, subject, body)

def receive_email(creds_path: str, email_id: str) -> str:
    """Receive a specific email.

    Args:
        creds_path (str): Path to Gmail API credentials file
        email_id (str): Gmail message ID to fetch

    Returns:
        str: Formatted email content or error description
    """
    service = get_gmail_service(creds_path)
    if isinstance(service, str):
        return f'Authentication error: {service}'
    result = gmail_client.get_email(service, email_id)
    if isinstance(result, str):
        return result
    try:
        email_msg = message_from_string(result.decode('utf-8'))
        formatted_content = []
        formatted_content.append(f"From: {email_msg['from']}")
        formatted_content.append(f"Subject: {email_msg['subject']}")
        formatted_content.append(f"To: {email_msg['to']}")
        formatted_content.append('\nBody:')
        if email_msg.is_multipart():
            for part in email_msg.walk():
                if part.get_content_type() == 'text/plain':
                    formatted_content.append(part.get_payload())
        else:
            formatted_content.append(email_msg.get_payload())
        return '\n'.join(formatted_content)
    except Exception as e:
        return f'Error parsing email content: {str(e)}'

def archive_email(creds_path: str, email_id: str) -> str:
    """Archive an email.

    Args:
        creds_path (str): Path to Gmail API credentials file
        email_id (str): ID of email to archive

    Returns:
        str: Success message or error description
    """
    gmail_id = email_id.replace('.eml', '') if email_id.endswith('.eml') else email_id
    service = get_gmail_service(creds_path)
    if isinstance(service, str):
        return f'Authentication error: {service}'
    return gmail_client.archive_email(service, gmail_id)

def list_emails(creds_path: str, query: str=None) -> str:
    """List emails in the inbox.

    Args:
        creds_path (str): Path to Gmail API credentials file
        query (str, optional): Gmail search query to filter results

    Returns:
        str: Newline-separated list of "sender: subject" or error message
    """
    service = get_gmail_service(creds_path)
    if isinstance(service, str):
        return f'Authentication error: {service}'
    return gmail_client.list_emails(service, query=query)