# Gmail Service Account Setup Instructions

## Overview
This guide explains how to set up a Google Cloud Service Account for automated Gmail access. This approach is ideal for LLM integration as it:
- Never requires browser interaction
- Has no token expiration issues
- Can access mailboxes without user intervention
- Provides stable, long-term automation capabilities

## Prerequisites
1. A Google Workspace (formerly G Suite) account with admin access
2. Access to Google Cloud Console
3. Gmail API enabled in your Google Cloud project

## Step-by-Step Setup

### 1. Create Service Account
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select or create your project
3. Navigate to "IAM & Admin" > "Service Accounts"
4. Click "Create Service Account"
5. Fill in:
   - Name: `gmail-automation`
   - ID: will be auto-generated
   - Description: "Service account for Gmail automation"
6. Click "Create and Continue"
7. Skip role assignment (roles will be handled via domain-wide delegation)
8. Click "Done"

### 2. Enable Domain-Wide Delegation
1. Find your service account in the list
2. Click on the email address
3. Go to "Keys" tab
4. Click "Add Key" > "Create new key"
5. Choose JSON format
6. Download and save as `service-credentials.json`
7. Go to "Details" tab
8. Click "Edit" (pencil icon)
9. Enable "Domain-wide Delegation"
10. Save

### 3. Configure Google Workspace
1. Go to [Google Workspace Admin Console](https://admin.google.com)
2. Navigate to Security > API Controls
3. Find "Domain-wide Delegation"
4. Click "Add new"
5. Enter:
   - Client ID: (from your service account)
   - OAuth Scopes (one per line):
     ```
     https://www.googleapis.com/auth/gmail.modify
     https://www.googleapis.com/auth/gmail.compose
     https://www.googleapis.com/auth/gmail.send
     ```
6. Click "Authorize"

### 4. Configure Application
1. Place `service-credentials.json` in your project root
2. Update email address in auth_service.py:
   ```python
   delegated_credentials = credentials.with_subject('your-user@your-domain.com')
   ```

## Verification
Run the verification tool:
```python
from auth_service import verify_service_account_setup
result = verify_service_account_setup('service-credentials.json')
print(result)
```

## Troubleshooting

### Common Issues:

1. "Permission denied" errors:
   - Verify scopes are correctly configured in Workspace Admin
   - Check service account has domain-wide delegation enabled
   - Ensure target user is in your Workspace domain

2. "Invalid grant" errors:
   - Verify client ID matches between service account and Workspace config
   - Check all required scopes are authorized

3. "File not found" errors:
   - Ensure service-credentials.json is in the correct location
   - Check file permissions

### Security Notes:
- Keep service-credentials.json secure - it grants significant access
- Use minimal required scopes
- Regularly audit service account usage
- Consider IP restrictions in production

## Migration from OAuth
To migrate from OAuth-based authentication:

1. Set up service account as above
2. Replace imports:
   ```python
   # from auth import get_gmail_service
   from auth_service import get_gmail_service
   ```
3. Update credential path:
   ```python
   service = get_gmail_service('service-credentials.json')
   ```

No other code changes should be needed as the service object interface remains the same.
