# Gmail Service Account Setup Instructions

NOTE: THIS GUIDE HAS NOT BEEN TESTED.

## Overview
This guide explains how to set up a Google Cloud Service Account for automated Gmail access. This approach is ideal for LLM integration as it:
- Never requires browser interaction
- Has no token expiration issues
- Can access mailboxes without user intervention
- Provides stable, long-term automation capabilities

## Prerequisites
Before beginning, ensure you have the following:

1. A Google Cloud Project: You'll need an active Google Cloud project. If you don't have one, create a new project. Note the project ID, as it will be needed throughout the setup.
2. Google Workspace Account with Admin Privileges: A Google Workspace account with administrator privileges is required for domain-wide delegation. This allows the service account to access Gmail on behalf of your organization.
3. Google Cloud Console Access: You need access to the Google Cloud Console to manage service accounts and APIs.
4. Enabled Gmail API: The Gmail API must be enabled within your Google Cloud project. You can enable this in the Google Cloud Console under APIs & Services.
5. Basic Python Knowledge: This guide assumes familiarity with basic Python concepts for configuring the application's authentication.

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

### 1.5 Enable Gmail API:
1. Go to project overview
2. Search for Gmail API
3. Click Enable

### 2. Enable Domain-Wide Delegation
1. Find your service account in the list
2. Click on the email address
3. Go to "Keys" tab
4. Click "Add Key" > "Create new key"
5. Choose JSON format
6. Download and save as `credentials.json`
6.5 If you see a message about key creation being disabled, " The organization policy constraint 'iam.disableServiceAccountKeyCreation' is enforced. This constraint disables the creation of new service account keys. "
   1- Go to google cloud
   2- Click to select the project/organization
   3- Click on "More Action" (the 3 points on the right side)
   4- Click on IAM/PERMISSIONS
   5- Edit your user and add Roles: "Organization Policy Administrator" and "Organization Administrator". (Note that Organization Policy Administrator should be visible at this level, if you are at the project level, this policy won't be available in the list).
   6- Now with those 2 roles, click on "Organization Policies" under IAM & Admin or repeat points 2/3 above and then select "Organization Policies".
   7- Search for "Disable service account key creation" and you should be able to click on Edit Policy and change the rule.

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

1. Place your service account key file as `__credentials.json` in your project root
2. Update email address in auth.py:
   ```python
   delegated_credentials = credentials.with_subject('your-user@your-domain.com')
   ```
3. Verify setup by running the test suite:
   ```bash
   pytest test_auth.py -v
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
