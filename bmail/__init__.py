"""
bmail - A simple Gmail client library designed for LLM integration
"""

from .llm_email_tools import (
    send_email,
    reply_to_email,
    check_inbox,
    read_email,
    archive_emails
)

__version__ = "0.1.0"
__author__ = "Ben Buzzell"
__email__ = "benbuzz790@gmail.com"

__all__ = [
    'send_email',
    'reply_to_email',
    'check_inbox',
    'read_email',
    'archive_emails',
]
