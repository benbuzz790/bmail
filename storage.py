import os
from pathlib import Path
from typing import Union


def _ensure_folder_exists(folder: str) ->str:
    """
    Ensures the specified folder exists, creating it if necessary.
    
    Args:
        folder: Name of the folder to check/create
        
    Returns:
        str: Success or error message
    """
    if folder not in ['inbox', 'sent', 'archive']:
        return (
            f"Error: Invalid folder '{folder}'. Must be 'inbox', 'sent', or 'archive'"
            )
    try:
        Path(folder).mkdir(exist_ok=True)
        return f"Success: Folder '{folder}' is ready"
    except Exception as e:
        return f"Error: Could not create folder '{folder}': {str(e)}"


def _validate_email_id(email_id: str) ->str:
    """
    Validates email ID format and ensures it has .eml extension.
    
    Args:
        email_id: Email ID to validate
        
    Returns:
        str: Error message if invalid, empty string if valid
    """
    if not email_id:
        return 'Error: Email ID cannot be empty'
    if not email_id.endswith('.eml'):
        return 'Error: Email ID must end with .eml extension'
    if '/' in email_id or '\\' in email_id:
        return 'Error: Email ID cannot contain path separators'
    return ''


def save_email(folder: str, email_id: str, content: bytes) ->str:
    """
    Saves email content to specified folder.
    
    Args:
        folder: Destination folder ('inbox', 'sent', or 'archive')
        email_id: Unique email identifier with .eml extension
        content: Email content as bytes
        
    Returns:
        str: Success or error message
    """
    folder_check = _ensure_folder_exists(folder)
    if folder_check.startswith('Error'):
        return folder_check
    id_check = _validate_email_id(email_id)
    if id_check:
        return id_check
    try:
        file_path = Path(folder) / email_id
        with open(file_path, 'wb') as f:
            f.write(content)
        return f'Success: Email saved to {file_path}'
    except Exception as e:
        return f'Error: Failed to save email: {str(e)}'


def read_email(folder: str, email_id: str) ->Union[bytes, str]:
    """
    Reads email content from specified folder.
    
    Args:
        folder: Source folder ('inbox', 'sent', or 'archive')
        email_id: Email identifier with .eml extension
        
    Returns:
        Union[bytes, str]: Email content as bytes if successful, error message as str if failed
    """
    folder_check = _ensure_folder_exists(folder)
    if folder_check.startswith('Error'):
        return folder_check
    id_check = _validate_email_id(email_id)
    if id_check:
        return id_check
    try:
        file_path = Path(folder) / email_id
        if not file_path.exists():
            return f'Error: Email {email_id} not found in {folder}'
        with open(file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        return f'Error: Failed to read email: {str(e)}'


def move_email(source_folder: str, dest_folder: str, email_id: str) ->str:
    """
    Moves email between folders.
    
    Args:
        source_folder: Source folder ('inbox', 'sent', or 'archive')
        dest_folder: Destination folder ('inbox', 'sent', or 'archive')
        email_id: Email identifier with .eml extension
        
    Returns:
        str: Success or error message
    """
    src_check = _ensure_folder_exists(source_folder)
    if src_check.startswith('Error'):
        return src_check
    dst_check = _ensure_folder_exists(dest_folder)
    if dst_check.startswith('Error'):
        return dst_check
    id_check = _validate_email_id(email_id)
    if id_check:
        return id_check
    try:
        source_path = Path(source_folder) / email_id
        dest_path = Path(dest_folder) / email_id
        if not source_path.exists():
            return f'Error: Email {email_id} not found in {source_folder}'
        if dest_path.exists():
            return f'Error: Email {email_id} already exists in {dest_folder}'
        os.rename(source_path, dest_path)
        return (
            f'Success: Moved {email_id} from {source_folder} to {dest_folder}')
    except Exception as e:
        return f'Error: Failed to move email: {str(e)}'


def list_emails(folder: str) ->str:
    """
    Lists emails in specified folder.
    
    Args:
        folder: Folder to list ('inbox', 'sent', or 'archive')
        
    Returns:
        str: Newline-separated list of email IDs or error message
    """
    folder_check = _ensure_folder_exists(folder)
    if folder_check.startswith('Error'):
        return folder_check
    try:
        path = Path(folder)
        files = [f.name for f in path.glob('*.eml')]
        if not files:
            return f'No emails found in {folder}'
        return '\n'.join(sorted(files))
    except Exception as e:
        return f'Error: Failed to list emails: {str(e)}'


def delete_email(folder: str, email_id: str) ->str:
    """
    Deletes specified email.
    
    Args:
        folder: Folder containing the email ('inbox', 'sent', or 'archive')
        email_id: Email identifier with .eml extension
        
    Returns:
        str: Success or error message
    """
    folder_check = _ensure_folder_exists(folder)
    if folder_check.startswith('Error'):
        return folder_check
    id_check = _validate_email_id(email_id)
    if id_check:
        return id_check
    try:
        file_path = Path(folder) / email_id
        if not file_path.exists():
            return f'Error: Email {email_id} not found in {folder}'
        os.remove(file_path)
        return f'Success: Deleted {email_id} from {folder}'
    except Exception as e:
        return f'Error: Failed to delete email: {str(e)}'
