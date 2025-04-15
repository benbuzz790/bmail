import os.path
import pickle
from typing import Union
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.discovery import Resource
from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource

def get_gmail_service(credentials_path: str, delegated_email: str) -> Union[Resource, str]:
    """Get an authenticated Gmail API service object using service account credentials.

    Args:
        credentials_path (str): Path to the service account JSON key file
        delegated_email (str, optional): Email address to delegate access to. If None, uses config default.

    Returns:
        Union[Resource, str]: Either an authenticated Gmail service object or an error message

    Note:
        This function expects a properly configured service account with:
        1. Domain-wide delegation enabled
        2. Required Gmail API scopes authorized in Google Workspace
    """
    if not os.path.exists(credentials_path):
        return f'Error: Credentials file not found at {credentials_path}'
    try:
        SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.send']
        credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
        delegated_credentials = credentials.with_subject(delegated_email)
        service = build('gmail', 'v1', credentials=delegated_credentials)
        try:
            service.users().getProfile(userId='me').execute()
            return service
        except Exception as e:
            return f'Error verifying service: {str(e)}'
    except Exception as e:
        return f'Error during authentication: {str(e)}'
