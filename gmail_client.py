from typing import Union
from googleapiclient.discovery import Resource
import base64
from email import message_from_bytes, message_from_string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header


def send_gmail(service: Resource, to_addr: str, cc: str, bcc: str, subject:
    str, body: str) ->str:
    """
    Send an email using Gmail API.
    
    Args:
        service: Authenticated Gmail API service object
        to_addr: Recipient email address
        cc: CC recipients (comma-separated)
        bcc: BCC recipients (comma-separated)
        subject: Email subject
        body: Email body text
    
    Returns:
        str: Success message or error description
    """
    try:
        profile = service.users().getProfile(userId='me').execute()
        from_addr = profile['emailAddress']
        message = MIMEMultipart()
        message['from'] = from_addr
        message['to'] = to_addr
        message['subject'] = subject
        if cc:
            message['cc'] = cc
        if bcc:
            message['bcc'] = bcc
        message.attach(MIMEText(body, 'plain'))
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        result = service.users().messages().send(userId='me', body={'raw': raw}
            ).execute()
        return f"Email sent successfully. Message ID: {result.get('id')}"
    except Exception as e:
        return f'Failed to send email: {str(e)}'


def get_email(service: Resource, email_id: str) ->Union[bytes, str]:
    """
    Retrieve email content in .eml format.
    
    Args:
        service: Authenticated Gmail API service object
        email_id: ID of the email to retrieve
    
    Returns:
        Union[bytes, str]: Email content in .eml format or error message
    """
    try:
        message = service.users().messages().get(userId='me', id=email_id,
            format='raw').execute()
        msg_bytes = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        return msg_bytes
    except Exception as e:
        return f'Failed to retrieve email: {str(e)}'


def list_emails(service: Resource, query: str=None, max_results: int=20) ->str:
    """
    List available emails in format "sender: subject".

    Args:
        service: Authenticated Gmail API service object
        query: Optional Gmail search query (e.g. 'subject:TEST')
        max_results: Maximum number of emails to list (default 20)

    Returns:
        str: Newline-separated list of "sender: subject" or error message
    """
    try:
        params = {'userId': 'me', 'maxResults': max_results}
        if query:
            params['q'] = query
        results = service.users().messages().list(**params).execute()
        messages = results.get('messages', [])
        if not messages:
            return 'No emails found'
        email_list = []
        for msg in messages:
            message = service.users().messages().get(userId='me', id=msg[
                'id'], format='full').execute()
            headers = message['payload']['headers']
            subject = 'No Subject'
            sender = 'Unknown Sender'
            for header in headers:
                if header['name'].lower() == 'subject':
                    subject = header['value']
                elif header['name'].lower() == 'from':
                    sender = header['value']
            email_list.append(f'{sender}: {subject}')
        return '\n'.join(email_list)
    except Exception as e:
        return f'Failed to list emails: {str(e)}'


def archive_email(service: Resource, email_id: str) ->str:
    """
    Archive/delete an email.
    
    Args:
        service: Authenticated Gmail API service object
        email_id: ID of the email to archive
    
    Returns:
        str: Success message or error description
    """
    try:
        service.users().messages().modify(userId='me', id=email_id, body={
            'removeLabelIds': ['INBOX']}).execute()
        return f'Email {email_id} archived successfully'
    except Exception as e:
        return f'Failed to archive email: {str(e)}'
