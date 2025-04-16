"""
bmail - A simple Gmail client library designed for LLM integration
"""
import os
from bmail import llm_email_tools

__version__ = '0.1.0'
__author__ = 'Ben Rinauto'
__all__ = ['llm_email_tools']

# Used for sending emails - not author email
__email__ = os.environ['BMAIL_SENDER']
