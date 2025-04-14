from typing import Optional
from bmail import email_handler


def send_email(cred_filepath: str, to: str, cc: str, bcc: str, subject: str,
    body: str) ->str:
    """Send an email using Gmail API.
    
    Args:
        cred_filepath: Path to credentials.json file
        to: Recipient email address
        cc: Comma-separated CC addresses (can be empty)
        bcc: Comma-separated BCC addresses (can be empty)
        subject: Email subject line
        body: Email body text
        
    Returns:
        str: Success/error message
    
    Example:
        >>> send_email("credentials.json", "user@example.com", "", "", "Hello", "Test message")
        "Email sent successfully"
    """
    return email_handler.send_email(cred_filepath, to, cc, bcc, subject, body)


def reply_to_email(cred_filepath: str, email_id: str, body: str) ->str:
    """Reply to a specific email using Gmail API.
    
    Args:
        cred_filepath: Path to credentials.json file
        email_id: Unique identifier of the email to reply to
        body: Reply message body
        
    Returns:
        str: Success/error message
    
    Example:
        >>> reply_to_email("credentials.json", "12345", "Thanks for your email")
        "Reply sent successfully"
    """
    receive_result = email_handler.receive_email(cred_filepath, email_id)
    if receive_result.startswith('Error'):
        return receive_result
    return email_handler.send_email(cred_filepath, 'benbuzz790@gmail.com',
        '', '', 'Re: TEST EMAIL', body)


def check_inbox(cred_filepath: str, query: str=None) ->str:
    """List inbox contents using Gmail API.

    Args:
        cred_filepath: Path to credentials.json file
        query: Optional Gmail search query (e.g. 'subject:"TEST EMAIL"')

    Returns:
        str: Newline-separated list of "sender: subject"

    Example:
        >>> check_inbox("credentials.json")
        "user1@example.com: Hello
user2@example.com: Meeting"
        >>> check_inbox("credentials.json", query='subject:"TEST EMAIL"')
        "test@example.com: TEST EMAIL"
    """
    return email_handler.list_emails(cred_filepath, query=query)


def read_email(cred_filepath: str, email_id: str) ->str:
    """Retrieve content of a specific email using Gmail API.
    
    Args:
        cred_filepath: Path to credentials.json file
        email_id: Unique identifier of the email to read
        
    Returns:
        str: Formatted email content
    
    Example:
        >>> read_email("credentials.json", "12345")
        "From: user@example.com
Subject: Hello
Body: Test message"
    """
    return email_handler.receive_email(cred_filepath, email_id)


def archive_emails(cred_filepath: str, email_id: str) ->str:
    """Archive a specific email using Gmail API.
    
    Args:
        cred_filepath: Path to credentials.json file
        email_id: Unique identifier of the email to archive
        
    Returns:
        str: Success/error message
    
    Example:
        >>> archive_emails("credentials.json", "12345")
        "Email archived successfully"
    """
    return email_handler.archive_email(cred_filepath, email_id)
