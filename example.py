import os.path
import pickle
from email import message_from_bytes
from email.header import decode_header
import base64
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail():
    """Authenticate the user and return the Gmail service."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json'
                , SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_messages(service, max_results=10):
    """Retrieve a list of messages."""
    results = service.users().messages().list(userId='me', maxResults=
        max_results).execute()
    messages = results.get('messages', [])
    return messages


def get_message_details(service, msg_id):
    """Get details of a specific message."""
    msg = service.users().messages().get(userId='me', id=msg_id, format='raw'
        ).execute()
    msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    mime_msg = message_from_bytes(msg_str)
    subject = mime_msg.get('Subject', 'No Subject')
    sender = mime_msg.get('From', 'Unknown Sender')
    if subject != 'No Subject':
        decoded_subject = decode_header(subject)
        subject = ''
        for part, charset in decoded_subject:
            if isinstance(part, bytes):
                subject += part.decode(charset if charset else 'utf-8')
            else:
                subject += str(part)
    if sender != 'Unknown Sender':
        decoded_sender = decode_header(sender)
        sender = ''
        for part, charset in decoded_sender:
            if isinstance(part, bytes):
                sender += part.decode(charset if charset else 'utf-8')
            else:
                sender += str(part)
    return {'subject': subject, 'sender': sender}


def main():
    service = authenticate_gmail()
    messages = get_messages(service)
    if not messages:
        print('No messages found.')
        return
    print(f'Displaying the latest {len(messages)} emails:\n')
    for msg in messages:
        details = get_message_details(service, msg['id'])
        print(f"From: {details['sender']}")
        print(f"Subject: {details['subject']}\n")


if __name__ == '__main__':
    main()
