import os
import pickle
from typing import Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource


def get_test_service() ->Resource:
    """Get a cached Gmail service for testing.
    
    Returns:
        Resource: Authenticated Gmail service object
        
    Note:
        This implementation caches the service object globally for test reuse.
        Only creates a new service if one doesn't exist or if credentials are invalid.
    """
    global _CACHED_SERVICE
    if _CACHED_SERVICE is not None:
        return _CACHED_SERVICE
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
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json'
                , SCOPES)
            creds = flow.run_local_server(port=0)
        import stat
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        os.chmod('token.pickle', stat.S_IRUSR | stat.S_IWUSR)
    _CACHED_SERVICE = build('gmail', 'v1', credentials=creds)
    return _CACHED_SERVICE
