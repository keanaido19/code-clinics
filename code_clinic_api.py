"""
Google calendar API calls.

"""

from googleapiclient.discovery import build
import helpers
import itertools


def build_calendar_service(token_creds):
    """
    Builds the calendar service
    """

    return build('calendar', 'v3', credentials=token_creds)

def get_calendar_data(calendar_service):
    """
    get the calendar data for a given number of days
    """
    
    now, end = helpers.get_date_range(7)
    
    return calendar_service.events().list(
        calendarId='primary', 
        timeMin=now, 
        timeMax=end,
        singleEvents=True,
        orderBy='startTime').execute()

def get_calendar_events(calendar_data):
    '''
    This Function returns the events that a in a calendar
    '''
    calendar_events = calendar_data.get('items', [])
    for calendar_event in calendar_events:
        helpers.format_calendar_event(calendar_event)
    return calendar_event

def format_calendar_events(calendar_events):
    '''
    Formats the way that calendar events are returned to user.
    '''
    grouped_calendar_events = itertools.groupby(calendar_events,key= lambda x: x['start']['event_date'])
    return {key:[value for value in values] for key,values in grouped_calendar_events}

def get_formated_calendar_events(token_credentials):
    '''
    Retrieves the events and returns them in a formated form.
    '''
    calendar_service = build_calendar_service(token_credentials)
    calendar_data = get_calendar_data(calendar_service)
    calendar_events = get_calendar_events(calendar_data)
    return format_calendar_events(calendar_events)