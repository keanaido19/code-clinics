"""
Additional functions to assist other modules.
"""

import datetime
from pytz import timezone

def get_current_utc_date():
    """
    Get the current date in utc format
    """
    return datetime.datetime.utcnow()

def get_new_utc_date(days):
    """
    Returns current utc date plus number of specified days
    """

    return get_current_utc_date() + datetime.timedelta(days= days) 

def get_date_range(days):
    """
    Returns a range of how many days will be displayed in the calendar 
    """
    start_date = get_current_utc_date().isoformat + 'Z'
    end_date = get_new_utc_date(days).isoformat + 'Z'
    return start_date,end_date

def convert_to_local_timezone(date):
    '''
    Converts date to local timezone
    '''
    timestamp = date.timestamp()
    utc_date = datetime.datetime.utcfromtimestamp(timestamp)
    return timezone('UTC').localize(utc_date).astimezone(timezone('Africa/Johannesburg'))

def get_calendar_event_start(calendar_event):
    '''
    Get the calendar event start date
    '''
    dt = datetime.datetime
    start_time = calendar_event['start'].get('dateTime', calendar_event['start'].get('date'))
    return convert_to_local_timezone(dt.fromisoformat(start_time))

def get_calendar_event_end(calendar_event):
    '''
    Get the calendar event start date
    '''
    dt = datetime.datetime
    end_time = calendar_event['end'].get('dateTime', calendar_event['end'].get('date'))
    return convert_to_local_timezone(dt.fromisoformat(end_time))

def format_calendar_event_start(calendar_event):
    '''
    formats the  calendar event start date
    '''
    event_start = get_calendar_event_start(calendar_event)
    calendar_event['start']['event_date'] = event_start.strftime('%a %d-%b-%Y')
    calendar_event['start']['event_time'] = event_start.strftime('%H:%M')

def format_calendar_event_end(calendar_event):
    '''
    formats the  calendar event start date
    '''
    event_end = get_calendar_event_end(calendar_event)
    calendar_event['end']['event_date'] = event_end.strftime('%a %d-%b-%Y')
    calendar_event['end']['event_time'] = event_end.strftime('%H:%M %p')

def format_calendar_event(calendar_event):
    '''
    formats the  calendar event start and end date
    '''
    format_calendar_event_start(calendar_event)
    format_calendar_event_end(calendar_event)