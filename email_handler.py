import os
from typing import Union
from email import message_from_string
from email.message import EmailMessage
from email.mime.text import MIMEText
import base64
from auth import get_gmail_service
import storage
import gmail_client


def send_email(creds_path: str, to_addr: str, cc: str, bcc: str, subject:
    str, body: str) ->str:
    """Send an email using Gmail API and store a copy in sent folder.
    
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
    result = gmail_client.send_gmail(service, to_addr, cc, bcc, subject, body)
    if not result.startswith('Email sent successfully'):
        return result
    msg_id = result.split('Message ID: ')[1]
    email_id = f'{msg_id}.eml'
    message = EmailMessage()
    message['To'] = to_addr
    if cc:
        message['Cc'] = cc
    if bcc:
        message['Bcc'] = bcc
    message['Subject'] = subject
    message.set_content(body)
    save_result = storage.save_email('sent', email_id, message.as_bytes())
    if save_result.startswith('Error'):
        return f'Email sent but failed to store locally: {save_result}'
    return result


def receive_email(creds_path: str, email_id: str) ->str:
    """Receive a specific email and store it in the inbox.

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
    storage_id = f'{email_id}.eml'
    save_result = storage.save_email('inbox', storage_id, result)
    if save_result.startswith('Error'):
        return f'Email retrieved but failed to store locally: {save_result}'
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


def archive_email(creds_path: str, email_id: str) ->str:
    """Move an email to the archive folder.
    
    Args:
        creds_path (str): Path to Gmail API credentials file
        email_id (str): ID of email to archive
    
    Returns:
        str: Success message or error description
    """
    gmail_id = email_id.replace('.eml', '') if email_id.endswith('.eml'
        ) else email_id
    storage_id = f'{gmail_id}.eml'
    service = get_gmail_service(creds_path)
    if isinstance(service, str):
        return f'Authentication error: {service}'
    result = gmail_client.archive_email(service, gmail_id)
    if not result.endswith('archived successfully'):
        return result
    move_result = storage.move_email('inbox', 'archive', storage_id)
    if move_result.startswith('Error'):
        return (
            f'Email archived in Gmail but failed to move locally: {move_result}'
            )
    return f'Email {gmail_id} archived successfully'


def list_emails(creds_path: str, query: str=None) ->str:
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
