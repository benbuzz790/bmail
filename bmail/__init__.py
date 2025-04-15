"""
bmail - A simple Gmail client library designed for LLM integration
"""
from bmail.llm_email_tools import send_email, reply_to_email, check_inbox, read_email, archive_emails
from .config import Config
__version__ = '0.1.0'
__author__ = 'Ben Rinauto'
__email__ = Config.DEFAULT_SENDER
__all__ = ['send_email', 'reply_to_email', 'check_inbox', 'read_email', 'archive_emails']
