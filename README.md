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
- email-validator

Note: google-auth-oauthlib is no longer required as we use service account authentication.

## Setup

### 1. Service Account Setup

This library uses a service account for authentication. Follow the detailed instructions in [service-setup-instructions.md](service-setup-instructions.md) to:
- Create a Google Cloud Project
- Set up a service account
- Enable domain-wide delegation
- Configure necessary permissions

### 2. Configuration

Configure the library using environment variables:

```bash
# Required configuration:
export BMAIL_CREDENTIALS_PATH="/path/to/your/credentials.json"  # Path to service account key file
export BMAIL_TEST_EMAIL="your.test@email.com"                  # Email used for testing
export BMAIL_SENDER="your.bot@email.com"                       # Default sender email for the bot
```

If not set, the library defaults to:
- BMAIL_CREDENTIALS_PATH: Looking for "__credentials.json" in project root
- BMAIL_TEST_EMAIL: "ben.rinauto@brwspace.com"
- BMAIL_SENDER: "claude.bot@brwspace.com"

3. Verify setup by running the test suite:
   ```bash
   pytest test_auth.py -v
   ```

## Usage Examples

### Send an Email
```python
response = client.send_email(
    to="recipient@example.com",
    subject="TEST EMAIL",
    body="Hello from LLM Email System!"
)
print(response)  # "Email sent successfully"
```

### Check Inbox
```python
emails = client.check_inbox()
print(emails)
# Returns: List of email IDs and subjects
# ["1234:Test Subject", "5678:Another Email"]
```

### Read Email
```python
email_content = client.read_email("1234")
print(email_content)
# Returns: "From: sender@example.com\nSubject: Test Subject\n\nEmail body here"
```

### Reply to Email
```python
response = client.reply_to_email(
    email_id="1234",
    reply_text="Thank you for your message"
)
print(response)  # "Reply sent successfully"
```

### Archive Emails
```python
response = client.archive_emails(["1234", "5678"])
print(response)  # "Emails archived successfully"
```

## API Reference

### send_email
```python
def send_email(to: str, subject: str, body: str) -> str
```
- Parameters:
  - to: Recipient email address
  - subject: Email subject line
  - body: Plain text email body
- Returns: Success message or error description
- Common Errors:
  - "Invalid email address"
  - "Authentication failed"

### check_inbox
```python
def check_inbox() -> list[str]
```
- Parameters: None
- Returns: List of "id:subject" strings
- Common Errors:
  - "Failed to fetch inbox"
  - "Authentication failed"

### read_email
```python
def read_email(email_id: str) -> str
```
- Parameters:
  - email_id: ID from check_inbox
- Returns: Formatted email content as string
- Common Errors:
  - "Email not found"
  - "Invalid email ID"

### reply_to_email
```python
def reply_to_email(email_id: str, reply_text: str) -> str
```
- Parameters:
  - email_id: ID from check_inbox
  - reply_text: Plain text reply body
- Returns: Success message or error description
- Common Errors:
  - "Email not found"
  - "Failed to send reply"

### archive_emails
```python
def archive_emails(email_ids: list[str]) -> str
```
- Parameters:
  - email_ids: List of IDs to archive
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
  ├── config.py            - Configuration (gitignored)
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
