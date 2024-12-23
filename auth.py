import os.path
import pickle
from typing import Union
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.discovery import Resource


def get_gmail_service(credentials_path: str) ->Union[Resource, str]:
    """Get an authenticated Gmail API service object.

    Args:
        credentials_path (str): Path to the credentials.json file

    Returns:
        Union[Resource, str]: Either an authenticated Gmail service object or an error message

    Note:
        This function is stateless and creates a new service object each time.
        It follows the exact authentication pattern from example.py.
    """
    if not os.path.exists(credentials_path):
        return f'Error: Credentials file not found at {credentials_path}'
    try:
        SCOPES = ['https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.compose',
            'https://www.googleapis.com/auth/gmail.send']
        creds = None
        if os.path.exists('token.pickle'):
            try:
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            except (EOFError, pickle.UnpicklingError):
                os.remove('token.pickle')
                creds = None
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            import stat
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
            os.chmod('token.pickle', stat.S_IRUSR | stat.S_IWUSR)
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        return f'Error during authentication: {str(e)}'
