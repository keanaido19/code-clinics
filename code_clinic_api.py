"""
Google calendar API calls.

"""

from googleapiclient.discovery import build


def build_calendar_service(token_creds):
    """
    Builds the calendar service
    """

    return build('calendar', 'v3', credentials=token_creds)
