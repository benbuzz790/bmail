from typing import Union
from googleapiclient.discovery import Resource
import base64
from email import message_from_bytes, message_from_string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header

def send_gmail(service: Resource, to_addr: str, cc: str, bcc: str, subject: str, body: str, thread_id: str=None, in_reply_to: str=None, references: str=None) -> str:
    """
    Send an email using Gmail API.

    Args:
        service: Authenticated Gmail API service object
        to_addr: Recipient email address
        cc: CC recipients (comma-separated)
        bcc: BCC recipients (comma-separated)
        subject: Email subject
        body: Email body text
        thread_id: Optional Gmail thread ID to reply to
        in_reply_to: Optional Message-ID being replied to
        references: Optional References header for threading

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
        if in_reply_to:
            message['In-Reply-To'] = in_reply_to
        if references:
            message['References'] = references
        message.attach(MIMEText(body, 'plain'))
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        params = {'userId': 'me'}
        if thread_id:
            params['body'] = {'raw': raw, 'threadId': thread_id}
        else:
            params['body'] = {'raw': raw}
        result = service.users().messages().send(**params).execute()
        return f"Email sent successfully. Message ID: {result.get('id')}"
    except Exception as e:
        return f'Failed to send email: {str(e)}'

def get_email(service: Resource, email_id: str) -> Union[tuple[bytes, dict], str]:
    """
    Retrieve email content and metadata.

    Args:
        service: Authenticated Gmail API service object
        email_id: ID of the email to retrieve

    Returns:
        Union[tuple[bytes, dict], str]: Tuple of (email content, metadata dict) or error message
    """
    try:
        message = service.users().messages().get(userId='me', id=email_id, format='full').execute()
        payload = message.get('payload', {})
        headers = payload.get('headers', [])
        email_msg = MIMEMultipart()
        for header in headers:
            name = header.get('name', '').lower()
            value = header.get('value', '')
            if name in ['from', 'to', 'subject', 'message-id', 'references']:
                email_msg[header['name']] = value
        if 'body' in payload and 'data' in payload['body']:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        else:
            parts = payload.get('parts', [])
            body = ''
            for part in parts:
                if part.get('mimeType') == 'text/plain' and 'data' in part.get('body', {}):
                    body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        email_msg.attach(MIMEText(body, 'plain'))
        metadata = {'thread_id': message.get('threadId'), 'message_id': next((h['value'] for h in headers if h['name'].lower() == 'message-id'), None), 'references': next((h['value'] for h in headers if h['name'].lower() == 'references'), '')}
        return (email_msg.as_bytes(), metadata)
    except Exception as e:
        return f'Failed to retrieve email: {str(e)}'

def list_emails(service: Resource, query: str=None, max_results: int=20) -> str:
    """
    List available emails in inbox in format "id:timestamp:subject".

    Args:
        service: Authenticated Gmail API service object
        query: Optional Gmail search query (e.g. 'subject:TEST')
        max_results: Maximum number of emails to list (default 20)

    Returns:
        str: Newline-separated list of "id:timestamp:subject" or error message
        Example: "abc123:2024-01-20 14:30:Test Subject"
    """
    try:
        search_query = 'in:inbox'
        if query:
            search_query = f'{search_query} {query}'
        params = {'userId': 'me', 'maxResults': max_results, 'q': search_query}
        results = service.users().messages().list(**params).execute()
        messages = results.get('messages', [])
        if not messages:
            return 'No emails found'
        email_list = []
        for msg in messages:
            message = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['subject', 'date']).execute()
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
            date = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')
            if not date and 'internalDate' in message:
                from datetime import datetime
                date = datetime.fromtimestamp(int(message['internalDate']) / 1000).strftime('%Y-%m-%d %H:%M')
            email_list.append(f"{msg['id']}:{date}:{subject}")
        return '\n'.join(email_list)
    except Exception as e:
        return f'Failed to list emails: {str(e)}'
        return '\n'.join(email_list)
    except Exception as e:
        return f'Failed to list emails: {str(e)}'
        messages = results.get('messages', [])
        if not messages:
            return 'No emails found'
        email_list = []
        for msg in messages:
            message = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            headers = message['payload']['headers']
            subject = 'No Subject'
            sender = 'Unknown Sender'
            for header in headers:
                if header['name'].lower() == 'subject':
                    subject = header['value']
                elif header['name'].lower() == 'from':
                    sender = header['value']
            email_list.append(f"{msg['id']}: {subject}")
        return '\n'.join(email_list)
    except Exception as e:
        return f'Failed to list emails: {str(e)}'

def archive_email(service: Resource, email_id: str) -> str:
    """
    Archive/delete an email.

    Args:
        service: Authenticated Gmail API service object
        email_id: ID of the email to archive

    Returns:
        str: Success message or error description
    """
    try:
        message = service.users().messages().get(userId='me', id=email_id).execute()
        current_labels = message.get('labelIds', [])
        if 'INBOX' not in current_labels:
            return f'Email {email_id} is not in inbox'
        result = service.users().messages().modify(userId='me', id=email_id, body={'removeLabelIds': ['INBOX']}).execute()
        updated_labels = result.get('labelIds', [])
        if 'INBOX' in updated_labels:
            return f'Failed to remove INBOX label from email {email_id}'
        return f'Email {email_id} archived successfully'
    except Exception as e:
        return f'Failed to archive email {email_id}: {str(e)}'