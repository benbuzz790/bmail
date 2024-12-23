import time
from auth import get_gmail_service
import gmail_client


def test_email_timing():
    """Test email send and list timing to find optimal delay."""
    print('Starting email timing test...')
    service = get_gmail_service('credentials.json')
    if isinstance(service, str):
        print(f'Service error: {service}')
        return
    test_email = 'benbuzz790@gmail.com'
    test_subject = 'TEST EMAIL TIMING'
    test_body = 'Testing email propagation timing.'
    print('\nSending email...')
    result = gmail_client.send_gmail(service, test_email, '', '',
        test_subject, test_body)
    print(f'Send result: {result}')
    delays = [2, 3, 5, 7, 10]
    for delay in delays:
        print(f'\nTesting {delay} second delay...')
        time.sleep(delay)
        print('Listing emails...')
        emails = gmail_client.list_emails(service)
        found = test_subject in emails
        print(f'Found test subject after {delay}s: {found}')
        if found:
            print('Email listing:')
            print(emails)
            return delay
    print('\nFailed to find test email in any attempt')
    return None
