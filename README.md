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
pip install -r requirements.txt
```

Dependencies:
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client
- email-validator

## Setup

1. Create a Google Cloud Project
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable the Gmail API

2. Get Credentials
   - Go to APIs & Services > Credentials
   - Create OAuth 2.0 Client ID
   - Download as credentials.json
   - Place in project root directory

3. Configure Authentication
   ```python
   # Follow example.py pattern:
   from email_client import EmailClient
   
   client = EmailClient()
   # First run will open browser for authentication
   # Tokens are saved locally for future use
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

Simple, flat directory structure:
- `email_client.py` - Main client implementation
- `example.py` - Authentication example
- `credentials.json` - OAuth credentials
- `requirements.txt` - Dependencies
- `README.md` - This documentation

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
   - Ensure credentials.json is in root directory
   - Follow example.py pattern exactly
   - Check Google Cloud Console settings

2. Rate Limits
   - Gmail API has usage quotas
   - Space out requests appropriately

3. Permission Issues
   - Ensure OAuth scope includes send/modify permissions
   - Re-authenticate if permissions change

4. Email Format
   - Use plain text only
   - Verify email addresses are valid
   - Keep subject lines reasonable length
