from typing import Union
from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource

def get_gmail_service(service_account_path: str, delegated_email: str=None) -> Union[Resource, str]:
    """Get an authenticated Gmail API service object using a service account.

    Args:
        service_account_path (str): Path to the service account JSON key file
            This should be a service account with domain-wide delegation enabled
            and the necessary Gmail API scopes pre-authorized in Google Workspace.
        delegated_email (str, optional): Email address to delegate access to. If None, uses config default.

    Returns:
        Union[Resource, str]: Either an authenticated Gmail service object or an error message

    Note:
        This implementation uses a service account with domain-wide delegation,
        which is ideal for automated/LLM usage as it:
        1. Never requires browser interaction
        2. Has no token expiration concerns
        3. Can access any authorized user's mailbox in the domain

    Setup Requirements:
        1. Create service account in Google Cloud Console
        2. Enable domain-wide delegation
        3. Download JSON key file
        4. Authorize service account in Google Workspace with scopes:
           - https://www.googleapis.com/auth/gmail.modify
           - https://www.googleapis.com/auth/gmail.compose
           - https://www.googleapis.com/auth/gmail.send
        5. Set user to impersonate (must be a user in your Google Workspace domain)
    """
    if delegated_email is None:
        from .config import Config
        delegated_email = Config.TEST_EMAIL
    try:
        SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.send']
        credentials = service_account.Credentials.from_service_account_file(service_account_path, scopes=SCOPES)
        delegated_credentials = credentials.with_subject(delegated_email)
        service = build('gmail', 'v1', credentials=delegated_credentials)
        return service
    except Exception as e:
        return f'Error during service account authentication: {str(e)}'

def verify_service_account_setup(service_account_path: str, delegated_email: str=None) -> str:
    """Verify that the service account is properly configured.

    Args:
        service_account_path (str): Path to the service account JSON key file
        delegated_email (str, optional): Email address to delegate access to. If None, uses config default.

    Returns:
        str: Success message or detailed error message explaining what's missing
    """
    if delegated_email is None:
        from .config import Config
        delegated_email = Config.TEST_EMAIL
    try:
        creds = service_account.Credentials.from_service_account_file(service_account_path)
        if not hasattr(creds, 'with_subject'):
            return 'Error: Service account does not have domain-wide delegation enabled. Please enable it in the Google Cloud Console.'
        service = get_gmail_service(service_account_path, delegated_email)
        if isinstance(service, str):
            return service
        result = service.users().getProfile(userId='me').execute()
        return f"Service account successfully configured with required permissions. Can access mailbox: {result.get('emailAddress')}"
    except Exception as e:
        return f'Service account configuration error: {str(e)}\n\n' + '\nRequired Setup Steps:\n1. Create service account in Google Cloud Console\n2. Enable domain-wide delegation\n3. Download JSON key file\n4. In Google Workspace Admin:\n   - Go to Security > API Controls > Domain-wide Delegation\n   - Add service account client ID\n   - Authorize these scopes:\n     * https://www.googleapis.com/auth/gmail.modify\n     * https://www.googleapis.com/auth/gmail.compose\n     * https://www.googleapis.com/auth/gmail.send\n'