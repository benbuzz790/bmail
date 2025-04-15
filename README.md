# bmail

A minimalist, string-based email client designed for LLM integration. This library is designed to be used with benbuzz790/bots via bot.add_tools(bmail.llm_email_tools)

As much as I tried, it doesn't "just work" - gmail has significant overhead and setup required before an automation can use your account.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Setup](#setup)
- [Usage Examples](#usage-examples)
- [API Reference](#api-reference)
- [File Structure](#file-structure)
- [Limitations](#limitations)
- [Troubleshooting](#troubleshooting)

## Overview

The LLM Email System is a simple, string-based email client specifically designed for Large Language Model (LLM) integration. It provides a clean interface to Gmail, focusing on core email operations through simple string inputs and outputs. Built to work seamlessly with the bots library, it emphasizes simplicity and reliability over complex features.

Key Features:
- Pure string-based interface
- Stateless operation
- Gmail API integration
- LLM-friendly design
- Minimal dependencies

## Installation

```bash
pip install git+https://github.com/benbuzz790/bmail.git
```

Dependencies:
- google-auth-httplib2
- google-api-python-client
- google-auth
- email-validator

## Setup

### 1. Service Account Setup

This library uses a service account for authentication. Follow the detailed instructions in [service-setup-instructions.md](service-setup-instructions.md) to:
- Create a Google Cloud Project
- Set up a service account
- Enable domain-wide delegation
- Configure necessary permissions

### 2. Configuration

The following environment variables are required:

```bash
# Required environment variables:
export BMAIL_CREDENTIALS_PATH="/path/to/your/credentials.json"  # Path to service account key file
export BMAIL_TEST_EMAIL="your.test@email.com"                  # Email used for testing
export BMAIL_SENDER="your.bot@email.com"                       # Email address used as the sender
```

These must be set before using the library. There are no default values.

3. Verify setup by running the test suite:
   ```bash
   pytest test_auth.py -v
   ```

## Usage Examples

### Send an Email
```python
from bmail import send_email

response = send_email(
    to="recipient@example.com",
    cc="",
    bcc="",
    subject="TEST EMAIL",
    body="Hello from LLM Email System!"
)
print(response)  # "Email sent successfully"
```

### Check Inbox
```python
from bmail import check_inbox

emails = check_inbox()  # Uses BMAIL_CREDENTIALS_PATH
print(emails)
# Returns: List of email IDs and subjects
# ["1234:Test Subject", "5678:Another Email"]
```

### Read Email
```python
from bmail import read_email

email_content = read_email("1234")  # Uses BMAIL_CREDENTIALS_PATH
print(email_content)
# Returns: "From: sender@example.com\nSubject: Test Subject\n\nEmail body here"
```

### Reply to Email
```python
from bmail import reply_to_email
import os

response = reply_to_email(
    email_id="1234",
    body="Thank you for your message",
    sender=os.environ['BMAIL_SENDER']
)
print(response)  # "Reply sent successfully"
```

### Archive Emails
```python
from bmail import archive_emails

response = archive_emails("1234")  # Uses BMAIL_CREDENTIALS_PATH
print(response)  # "Email archived successfully"
```

## API Reference

### send_email
```python
def send_email(to: str, cc: str, bcc: str, subject: str, body: str, cred_filepath: Optional[str] = None) -> str
```
- Parameters:
  - to: Recipient email address
  - cc: CC recipients (comma-separated)
  - bcc: BCC recipients (comma-separated)
  - subject: Email subject line
  - body: Plain text email body
  - cred_filepath: Optional path to credentials file (uses BMAIL_CREDENTIALS_PATH if not provided)
- Returns: Success message or error description
- Common Errors:
  - "Invalid email address"
  - "Authentication failed"

### check_inbox
```python
def check_inbox(query: str = None, cred_filepath: Optional[str] = None) -> str
```
- Parameters:
  - query: Optional Gmail search query
  - cred_filepath: Optional path to credentials file (uses BMAIL_CREDENTIALS_PATH if not provided)
- Returns: List of "id:subject" strings
- Common Errors:
  - "Failed to fetch inbox"
  - "Authentication failed"

### read_email
```python
def read_email(email_id: str, cred_filepath: Optional[str] = None) -> str
```
- Parameters:
  - email_id: ID from check_inbox
  - cred_filepath: Optional path to credentials file (uses BMAIL_CREDENTIALS_PATH if not provided)
- Returns: Formatted email content as string
- Common Errors:
  - "Email not found"
  - "Invalid email ID"

### reply_to_email
```python
def reply_to_email(email_id: str, body: str, sender: str, cred_filepath: Optional[str] = None) -> str
```
- Parameters:
  - email_id: ID from check_inbox
  - body: Plain text reply body
  - sender: Email address to send from (typically BMAIL_SENDER)
  - cred_filepath: Optional path to credentials file (uses BMAIL_CREDENTIALS_PATH if not provided)
- Returns: Success message or error description
- Common Errors:
  - "Email not found"
  - "Failed to send reply"

### archive_emails
```python
def archive_emails(email_id: str, cred_filepath: Optional[str] = None) -> str
```
- Parameters:
  - email_id: ID of email to archive
  - cred_filepath: Optional path to credentials file (uses BMAIL_CREDENTIALS_PATH if not provided)
- Returns: Success message or error description
- Common Errors:
  - "Invalid email ID"
  - "Failed to archive"

## File Structure

```
bmail/
  ├── __init__.py
  ├── auth.py              - Service account authentication
  ├── auth_service.py      - Gmail service setup
  ├── email_handler.py     - Core email operations
  ├── gmail_client.py      - Gmail API interface
  └── llm_email_tools.py   - LLM-friendly interface

tests/
  ├── test_auth.py
  ├── test_email_handler.py
  ├── test_gmail_client.py
  └── test_llm_email_tools.py

__credentials.json         - Service account key (gitignored)
README.md                  - This documentation
service-setup-instructions.md - Detailed setup guide
setup.py                   - Package configuration
```

## Limitations

Intentionally NOT Supported:
1. Attachments
2. Email templates
3. Multiple providers (Gmail only)
4. Advanced filtering
5. Unread status tracking
6. Custom exceptions
7. Logging
8. Thread safety

These limitations maintain simplicity and reliability.

## Troubleshooting

Common Issues:

1. Authentication Errors
   - Verify service account key file exists at BMAIL_CREDENTIALS_PATH
   - Check service account has domain-wide delegation enabled
   - Verify all required scopes are authorized in Google Workspace
   - Check Google Cloud Console API is enabled

2. Rate Limits
   - Gmail API has usage quotas
   - Space out requests appropriately

3. Permission Issues
   - Ensure service account has proper domain-wide delegation
   - Verify all required scopes are authorized:
     * https://www.googleapis.com/auth/gmail.modify
     * https://www.googleapis.com/auth/gmail.compose
     * https://www.googleapis.com/auth/gmail.send

4. Email Format
   - Use plain text only
   - Verify email addresses are valid
   - Keep subject lines reasonable length

5. Configuration Issues
   - Check environment variables are set correctly
   - Verify sender email has proper permissions
   - Ensure test email is in your workspace domain
